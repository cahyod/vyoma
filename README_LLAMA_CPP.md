# Vyoma AI Security Scanner - llama.cpp Integration

## Overview

Vyoma now supports **llama.cpp** integration with the **Qwen2.5-7B-Instruct** model (Q4_K_M quantization) as an alternative to Ollama. This provides better performance, offline capability, and more control over the AI inference process.

## Features

- **Model**: Qwen2.5-7B-Instruct.Q4_K_M.gguf
- **Size**: ~4GB (4-bit quantized)
- **Performance**: Excellent balance of speed and quality
- **Offline**: No external service required
- **Automatic Download**: Model is automatically downloaded from HuggingFace on first use

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `llama-cpp-python>=0.2.0` - Python bindings for llama.cpp
- `huggingface-hub>=0.20.0` - For downloading models from HuggingFace

### 2. System Requirements

- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: ~5GB free space for model
- **Python**: 3.8 or higher
- **OS**: Windows, Linux, or macOS

## Usage

### Basic Example

```python
import asyncio
from core.llama_cpp_engine import LlamaCppEngine

async def main():
    # Initialize engine
    engine = LlamaCppEngine()
    
    async with engine:
        # Generate SQL injection payloads
        target_info = {
            "url": "https://example.com/login",
            "database": "MySQL",
            "technologies": ["PHP", "Apache"]
        }
        
        payloads = await engine.generate_sql_payloads(target_info)
        print(f"Generated {len(payloads)} payloads")
        
        # Analyze vulnerability
        vuln_data = {
            "type": "SQL Injection",
            "severity": "High",
            "evidence": "Error message reveals database structure"
        }
        
        analysis = await engine.analyze_vulnerability(vuln_data)
        print(analysis)

asyncio.run(main())
```

### Advanced Configuration

```python
from core.llama_cpp_engine import LlamaCppEngine

# Use custom model path
engine = LlamaCppEngine(
    model_path="/path/to/custom/model.gguf",
    logger=my_logger
)

# The model will be loaded automatically on first use
# Or you can preload it:
await engine.load_model()
```

### Available Methods

The `LlamaCppEngine` class provides the same interface as `AIEngine`:

- `generate_sql_payloads(target_info)` - Generate SQL injection payloads
- `generate_xss_payloads(target_info)` - Generate XSS payloads
- `generate_command_injection_payloads(target_info)` - Generate command injection payloads
- `generate_ssrf_payloads(target_info)` - Generate SSRF payloads
- `analyze_vulnerability(vuln_data)` - Analyze a vulnerability
- `generate_chain_attack(vulnerabilities)` - Generate attack chain scenarios
- `generate_reconnaissance_analysis(recon_data)` - Analyze reconnaissance data
- `generate_executive_summary(scan_results)` - Generate executive summary
- `query_llama_async(prompt, system_prompt, temperature)` - Custom queries

## Model Information

### Qwen2.5-7B-Instruct

- **Base Model**: Qwen2.5-7B
- **Fine-tuning**: Instruction-tuned for better task following
- **Quantization**: Q4_K_M (4-bit K-quants medium)
- **Context Window**: 4096 tokens
- **License**: Apache 2.0

### Model Source

The model is downloaded from HuggingFace:
- **Repository**: `Qwen/Qwen2.5-7B-Instruct-GGUF`
- **File**: `qwen2.5-7b-instruct-q4_k_m.gguf`
- **Location**: `~/.vyoma/models/`

## Comparison: llama.cpp vs Ollama

| Feature | llama.cpp | Ollama |
|---------|-----------|--------|
| Setup | Automatic | Manual installation |
| Model Management | Automatic download | Manual pull |
| Performance | Optimized CPU | Good CPU/GPU |
| Offline | Fully offline | Requires service |
| Memory Usage | ~4-6GB | ~4-8GB |
| Context Length | Configurable | Fixed per model |
| GPU Support | Optional | Built-in |

## Troubleshooting

### Import Errors

If you get `ImportError: No module named 'llama_cpp'`:

```bash
pip install --upgrade llama-cpp-python
```

### Model Download Issues

If the model download fails:

1. Check your internet connection
2. Try manual download from HuggingFace:
   ```bash
   huggingface-cli download Qwen/Qwen2.5-7B-Instruct-GGUF qwen2.5-7b-instruct-q4_k_m.gguf --local-dir ~/.vyoma/models
   ```

### Out of Memory

If you run out of memory:

1. Close other applications
2. Use a smaller context window (modify `n_ctx` in `load_model()`)
3. Consider using Ollama with a smaller model

## Examples

See `examples/llama_cpp_example.py` for a complete working example.

## Migration from Ollama

If you're currently using Ollama, migration is simple:

```python
# Old code (Ollama)
from core.ai_engine import AIEngine
engine = AIEngine(model="llama3.2:3b")

# New code (llama.cpp)
from core.llama_cpp_engine import LlamaCppEngine
engine = LlamaCppEngine()

# Both engines have the same interface!
payloads = await engine.generate_sql_payloads(target_info)
```

## License

This integration uses models under Apache 2.0 license. See the model repository for full terms.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example code
3. Open an issue on GitHub
