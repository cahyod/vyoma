"""
Example: Using Vyoma with llama.cpp and Qwen2.5-7B-Instruct

This example demonstrates how to use the LlamaCppEngine for AI-powered
security testing with the Qwen2.5-7B-Instruct model.
"""

import asyncio
from core.llama_cpp_engine import LlamaCppEngine


async def main():
    """Demonstrate llama.cpp engine usage."""
    
    print("=" * 60)
    print("Vyoma AI Security Scanner - llama.cpp Integration Example")
    print("Model: Qwen2.5-7B-Instruct.Q4_K_M")
    print("=" * 60)
    
    # Initialize the engine
    engine = LlamaCppEngine()
    
    async with engine:
        # Validate connection (load model)
        print("\n[1] Validating model...")
        if not await engine.validate_connection():
            print("Failed to load model. Exiting.")
            return
        print("Model loaded successfully!")
        
        # Generate SQL injection payloads
        print("\n[2] Generating SQL injection payloads...")
        target_info = {
            "url": "https://example.com/login",
            "database": "MySQL",
            "technologies": ["PHP", "Apache"]
        }
        sql_payloads = await engine.generate_sql_payloads(target_info)
        print(f"Generated {len(sql_payloads)} payloads:")
        for i, payload in enumerate(sql_payloads[:3], 1):
            print(f"  {i}. {payload}")
        
        # Generate XSS payloads
        print("\n[3] Generating XSS payloads...")
        xss_payloads = await engine.generate_xss_payloads(target_info)
        print(f"Generated {len(xss_payloads)} payloads:")
        for i, payload in enumerate(xss_payloads[:3], 1):
            print(f"  {i}. {payload}")
        
        # Analyze a vulnerability
        print("\n[4] Analyzing vulnerability...")
        vuln_data = {
            "type": "SQL Injection",
            "severity": "High",
            "evidence": "Error message reveals database structure"
        }
        analysis = await engine.analyze_vulnerability(vuln_data)
        print("Analysis results:")
        print(f"  Explanation: {analysis.get('explanation', 'N/A')}")
        print(f"  Impact: {analysis.get('impact', 'N/A')}")
        print(f"  Remediation: {analysis.get('remediation', 'N/A')}")
        
        # Generate executive summary
        print("\n[5] Generating executive summary...")
        scan_results = {
            "target": "https://example.com",
            "risk_score": 75,
            "vulnerabilities": [
                {"type": "SQL Injection", "severity": "High"},
                {"type": "XSS", "severity": "Medium"},
                {"type": "CSRF", "severity": "Low"}
            ],
            "scan_duration": 120
        }
        summary = await engine.generate_executive_summary(scan_results)
        print("Executive Summary:")
        print(summary[:500] + "..." if len(summary) > 500 else summary)
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
