"""
LLama.cpp Engine for Vyoma Security Scanner

Handles all AI-related operations using llama.cpp with Qwen2.5-7B-Instruct model,
including payload generation, vulnerability analysis, and report summarization.

This engine provides an alternative to Ollama, using local GGUF models directly
via llama-cpp-python bindings for better performance and control.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor

from huggingface_hub import hf_hub_download


class LlamaCppEngine:
    """AI Engine using llama.cpp with Qwen2.5-7B-Instruct model.
    
    This class interfaces with llama.cpp to provide AI-powered security testing
    capabilities using the Qwen2.5-7B-Instruct model in GGUF format.
    
    Attributes:
        model_path: Path to the GGUF model file
        model_name: Name of the model being used
        logger: Logger instance for debug output
        llm: Loaded LLM instance from llama-cpp-python
        executor: Thread pool executor for async operations
    """
    
    MODEL_REPO = "Qwen/Qwen2.5-7B-Instruct-GGUF"
    MODEL_FILE = "qwen2.5-7b-instruct-q4_k_m.gguf"
    DEFAULT_MODEL_DIR = Path.home() / ".vyoma" / "models"
    
    def __init__(
        self, 
        model_path: Optional[str] = None,
        logger=None
    ):
        """Initialize the llama.cpp engine.
        
        Args:
            model_path: Path to the GGUF model file (auto-downloaded if not provided)
            logger: Logger instance for output
        """
        self.logger = logger
        self.model_path = model_path
        self.model_name = "Qwen2.5-7B-Instruct.Q4_K_M"
        self.llm = None
        self.executor = ThreadPoolExecutor(max_workers=1)
        self._model_loaded = False
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message using the provided logger or print."""
        if self.logger:
            if level == "ERROR":
                self.logger.error(message)
            elif level == "WARNING":
                self.logger.warning(message)
            else:
                self.logger.info(message)
        else:
            print(f"[{level}] {message}")
    
    def download_model(self) -> str:
        """Download the Qwen2.5-7B-Instruct model from HuggingFace.
        
        Returns:
            Path to the downloaded model file
            
        Raises:
            Exception: If download fails
        """
        try:
            self.log("Downloading Qwen2.5-7B-Instruct model from HuggingFace...")
            self.log("This is a one-time download (~4GB). Please wait...")
            
            # Create model directory if it doesn't exist
            self.DEFAULT_MODEL_DIR.mkdir(parents=True, exist_ok=True)
            
            # Download model from HuggingFace
            model_path = hf_hub_download(
                repo_id=self.MODEL_REPO,
                filename=self.MODEL_FILE,
                cache_dir=str(self.DEFAULT_MODEL_DIR),
                local_dir=str(self.DEFAULT_MODEL_DIR)
            )
            
            self.log(f"Model downloaded successfully to: {model_path}")
            return model_path
            
        except Exception as e:
            self.log(f"Failed to download model: {e}", "ERROR")
            raise
    
    def load_model(self) -> bool:
        """Load the GGUF model into memory.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            # Import llama_cpp here to avoid import errors if not installed
            from llama_cpp import Llama
            
            # Download model if path not provided
            if not self.model_path:
                self.model_path = self.download_model()
            elif not os.path.exists(self.model_path):
                self.log(f"Model file not found at {self.model_path}, downloading...", "WARNING")
                self.model_path = self.download_model()
            
            self.log(f"Loading model: {self.model_path}")
            
            # Load the model with optimized settings
            self.llm = Llama(
                model_path=str(self.model_path),
                n_ctx=4096,          # Context window size
                n_threads=4,         # Number of CPU threads
                n_gpu_layers=0,      # Set to >0 for GPU acceleration
                verbose=False
            )
            
            self._model_loaded = True
            self.log("Model loaded successfully!")
            return True
            
        except ImportError as e:
            self.log(f"llama-cpp-python not installed: {e}", "ERROR")
            self.log("Install with: pip install llama-cpp-python", "ERROR")
            return False
        except Exception as e:
            self.log(f"Failed to load model: {e}", "ERROR")
            return False
    
    def unload_model(self):
        """Unload the model from memory."""
        if self.llm:
            del self.llm
            self.llm = None
            self._model_loaded = False
            self.log("Model unloaded from memory")
    
    def query_llama(
        self, 
        prompt: str, 
        system_prompt: str = "", 
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """Query the model with a prompt.
        
        Args:
            prompt: User prompt to send
            system_prompt: System instruction for the model
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Model response text or empty string on error
        """
        if not self._model_loaded:
            if not self.load_model():
                return ""
        
        try:
            # Format prompt in chat format for Qwen
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Generate response
            response = self.llm.create_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,
                top_k=40
            )
            
            return response['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            self.log(f"Error generating response: {e}", "ERROR")
            return ""
    
    async def query_llama_async(
        self, 
        prompt: str, 
        system_prompt: str = "", 
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """Async wrapper for query_llama.
        
        Args:
            prompt: User prompt to send
            system_prompt: System instruction for the model
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Model response text or empty string on error
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            lambda: self.query_llama(prompt, system_prompt, temperature, max_tokens)
        )
    
    async def validate_connection(self) -> bool:
        """Validate that the model can be loaded.
        
        Returns:
            True if model can be loaded, False otherwise
        """
        try:
            if self._model_loaded:
                return True
            
            # Try to load the model
            return self.load_model()
            
        except Exception:
            return False
    
    async def generate_sql_payloads(self, target_info: Dict[str, Any]) -> List[str]:
        """Generate SQL injection payloads using AI.
        
        Args:
            target_info: Dictionary containing target URL, database type, and technologies
            
        Returns:
            List of SQL injection payloads (max 10)
        """
        system_prompt = (
            "You are a cybersecurity expert specializing in SQL injection testing. "
            "Generate creative and effective SQL injection payloads for penetration testing purposes only. "
            "Return only the payloads, one per line, without explanations."
        )
        
        prompt = f"""
Generate 10 advanced SQL injection payloads for testing the following target:

Target URL: {target_info.get('url', 'Unknown')}
Database Type: {target_info.get('database', 'Unknown')}
Technology Stack: {target_info.get('technologies', [])}

Include payloads for:
1. Union-based injection
2. Boolean-based blind injection
3. Time-based blind injection
4. Error-based injection
5. Second-order injection

Return only the payloads, one per line, without explanations.
"""
        
        response = await self.query_llama_async(prompt, system_prompt, temperature=0.8)
        payloads = [line.strip() for line in response.split('\n') if line.strip()]
        return payloads[:10]
    
    async def generate_xss_payloads(self, target_info: Dict[str, Any]) -> List[str]:
        """Generate XSS payloads using AI.
        
        Args:
            target_info: Dictionary containing target URL, content type, and security headers
            
        Returns:
            List of XSS payloads (max 10)
        """
        system_prompt = (
            "You are a cybersecurity expert specializing in XSS testing. "
            "Generate creative XSS payloads that can bypass modern filters and WAFs. "
            "Return only the payloads, one per line, without explanations."
        )
        
        prompt = f"""
Generate 10 advanced XSS payloads for testing the following target:

Target URL: {target_info.get('url', 'Unknown')}
Content-Type: {target_info.get('content_type', 'text/html')}
Security Headers: {target_info.get('security_headers', {})}

Include payloads for:
1. Filter bypass techniques
2. DOM-based XSS
3. Stored XSS
4. Reflected XSS
5. WAF evasion

Return only the payloads, one per line, without explanations.
"""
        
        response = await self.query_llama_async(prompt, system_prompt, temperature=0.8)
        payloads = [line.strip() for line in response.split('\n') if line.strip()]
        return payloads[:10]
    
    async def generate_command_injection_payloads(
        self, 
        target_info: Dict[str, Any]
    ) -> List[str]:
        """Generate command injection payloads using AI.
        
        Args:
            target_info: Dictionary containing target URL, OS, and server software
            
        Returns:
            List of command injection payloads (max 10)
        """
        system_prompt = (
            "You are a cybersecurity expert specializing in command injection testing. "
            "Generate effective command injection payloads for different operating systems. "
            "Return only the payloads, one per line, without explanations."
        )
        
        prompt = f"""
Generate 10 command injection payloads for testing the following target:

Target URL: {target_info.get('url', 'Unknown')}
Server OS: {target_info.get('os', 'Unknown')}
Server Software: {target_info.get('server', 'Unknown')}

Include payloads for:
1. Linux/Unix systems
2. Windows systems
3. Blind command injection
4. Time-based detection
5. Output redirection

Return only the payloads, one per line, without explanations.
"""
        
        response = await self.query_llama_async(prompt, system_prompt, temperature=0.8)
        payloads = [line.strip() for line in response.split('\n') if line.strip()]
        return payloads[:10]
    
    async def generate_ssrf_payloads(self, target_info: Dict[str, Any]) -> List[str]:
        """Generate SSRF payloads using AI.
        
        Args:
            target_info: Dictionary containing target URL, cloud provider, and internal networks
            
        Returns:
            List of SSRF payloads (max 10)
        """
        system_prompt = (
            "You are a cybersecurity expert specializing in SSRF testing. "
            "Generate SSRF payloads that can access internal services and cloud metadata. "
            "Return only the payloads, one per line, without explanations."
        )
        
        prompt = f"""
Generate 10 SSRF payloads for testing the following target:

Target URL: {target_info.get('url', 'Unknown')}
Cloud Provider: {target_info.get('cloud_provider', 'Unknown')}
Internal Networks: {target_info.get('internal_networks', [])}

Include payloads for:
1. AWS metadata access
2. Azure metadata access
3. GCP metadata access
4. Internal service discovery
5. Localhost bypass techniques

Return only the payloads, one per line, without explanations.
"""
        
        response = await self.query_llama_async(prompt, system_prompt, temperature=0.8)
        payloads = [line.strip() for line in response.split('\n') if line.strip()]
        return payloads[:10]
    
    async def analyze_vulnerability(
        self, 
        vuln_data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Analyze a vulnerability using AI (optimized for speed).
        
        Args:
            vuln_data: Dictionary containing vulnerability details
            
        Returns:
            Dictionary with explanation, impact, remediation, prevention, and CVSS score
        """
        system_prompt = (
            "You are a cybersecurity expert. Provide concise vulnerability analysis. "
            "Keep responses brief and actionable."
        )
        
        prompt = f"""
Vulnerability: {vuln_data.get('type', 'Unknown')} ({vuln_data.get('severity', 'Unknown')})
Evidence: {vuln_data.get('evidence', 'None')}

Provide brief analysis:
1. Risk explanation (2 sentences)
2. Impact (1 sentence) 
3. Fix (1 sentence)
4. CVSS score (number only)

Keep response under 100 words total.
"""
        
        response = await self.query_llama_async(prompt, system_prompt, temperature=0.1)
        
        lines = response.strip().split('\n')
        return {
            "explanation": lines[0] if len(lines) > 0 else "Vulnerability detected",
            "impact": lines[1] if len(lines) > 1 else "Potential security risk",
            "remediation": lines[2] if len(lines) > 2 else "Apply security patches",
            "prevention": "Follow security best practices",
            "cvss_score": "7.5"
        }
    
    async def generate_chain_attack(
        self, 
        vulnerabilities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate chain attack scenarios using AI.
        
        Args:
            vulnerabilities: List of discovered vulnerabilities
            
        Returns:
            List of attack chain scenarios
        """
        system_prompt = (
            "You are a cybersecurity expert specializing in advanced persistent threats. "
            "Analyze vulnerabilities and create realistic attack chain scenarios. "
            "Format your response as a JSON array."
        )
        
        vuln_summary = "\n".join([
            f"- {v.get('type', 'Unknown')}: {v.get('severity', 'Unknown')} ({v.get('url', 'Unknown')})"
            for v in vulnerabilities
        ])
        
        prompt = f"""
Given the following vulnerabilities, create realistic attack chain scenarios:

{vuln_summary}

For each attack chain:
1. List the vulnerabilities used in order
2. Describe the attack steps
3. Explain the final objective
4. Assess the overall impact

Generate up to 3 attack chains. Format as JSON array with objects containing:
chain_id, vulnerabilities_used, attack_steps, objective, impact

Return ONLY the JSON array, no other text.
"""
        
        response = await self.query_llama_async(prompt, system_prompt, temperature=0.6)
        
        # Try to extract JSON from response
        try:
            # Find JSON array in response
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                chains = json.loads(json_str)
                return chains if isinstance(chains, list) else []
        except json.JSONDecodeError:
            pass
        
        return []
    
    async def generate_reconnaissance_analysis(
        self, 
        recon_data: Dict[str, Any]
    ) -> str:
        """Generate reconnaissance analysis using AI.
        
        Args:
            recon_data: Dictionary containing reconnaissance data
            
        Returns:
            AI-generated analysis text
        """
        system_prompt = (
            "You are a cybersecurity expert analyzing reconnaissance data. "
            "Provide insights about the target's security posture and potential attack vectors."
        )
        
        prompt = f"""
Analyze the following reconnaissance data and provide security insights:

Target: {recon_data.get('target', 'Unknown')}
Technologies: {recon_data.get('technologies', [])}
Open Ports: {recon_data.get('open_ports', [])}
Subdomains: {recon_data.get('subdomains', [])}
Security Headers: {recon_data.get('security_headers', {})}
SSL/TLS Info: {recon_data.get('ssl_info', {})}

Provide:
1. Security posture assessment
2. Potential attack vectors
3. Technology-specific risks
4. Recommendations for further testing
5. Priority areas for security improvement

Be specific and actionable in your analysis.
"""
        
        return await self.query_llama_async(prompt, system_prompt, temperature=0.4)
    
    async def generate_executive_summary(
        self, 
        scan_results: Dict[str, Any]
    ) -> str:
        """Generate executive summary using AI.
        
        Args:
            scan_results: Dictionary containing complete scan results
            
        Returns:
            AI-generated executive summary text
        """
        system_prompt = (
            "You are a cybersecurity consultant writing an executive summary for C-level executives. "
            "Focus on business impact, risk levels, and strategic recommendations."
        )
        
        vulnerabilities = scan_results.get('vulnerabilities', [])
        risk_score = scan_results.get('risk_score', 0)
        
        vuln_counts = {}
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'Unknown')
            vuln_counts[severity] = vuln_counts.get(severity, 0) + 1
        
        prompt = f"""
Create an executive summary for a security assessment with the following results:

Target: {scan_results.get('target', 'Unknown')}
Risk Score: {risk_score}/100
Total Vulnerabilities: {len(vulnerabilities)}
Vulnerability Breakdown: {vuln_counts}
Scan Duration: {scan_results.get('scan_duration', 0)} seconds

Include:
1. Executive overview (2-3 sentences)
2. Key findings and business risks
3. Immediate action items
4. Strategic recommendations
5. Compliance implications (if any)

Keep it concise and business-focused.
"""
        
        return await self.query_llama_async(prompt, system_prompt, temperature=0.3)
    
    def __enter__(self):
        """Context manager entry - load model."""
        self.load_model()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - unload model."""
        self.unload_model()
    
    async def __aenter__(self):
        """Async context manager entry."""
        await asyncio.get_event_loop().run_in_executor(
            self.executor, self.load_model
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.unload_model()
