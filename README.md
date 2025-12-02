<div align="center">

![Vyoma Logo](logo.png)

# VYOMA AI Security Scanner

### Professional AI-Powered Web Application Security Testing Platform

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v1.0.0-orange.svg)](https://github.com/cahyod/vyoma)

**Enterprise-grade security scanner combining traditional penetration testing with AI analysis**

</div>

---

## 📖 Table of Contents

- [What is VYOMA?](#-what-is-vyoma)
- [Key Features](#-key-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [Usage Examples](#-usage-examples)
  - [Example 1: Quick Security Check](#example-1-quick-security-check)
  - [Example 2: Standard Security Assessment](#example-2-standard-security-assessment)
  - [Example 3: Thorough Security Audit](#example-3-thorough-security-audit)
  - [Example 4: Custom Testing](#example-4-custom-testing)
  - [Example 5: CI/CD Pipeline Integration](#example-5-cicd-pipeline-integration)
  - [Test Targets (For Practice)](#test-targets-for-practice)
- [Scan Modes](#-scan-modes)
- [Troubleshooting](#-troubleshooting)
- [Help & Support](#-help--support)
- [Legal Notice](#️-legal-notice)
- [Author](#-author)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 What is VYOMA?

**VYOMA** (Advanced Security Testing & Risk Assessment with Vulnerability Analysis) is a professional-grade AI-powered web application security scanner designed for:

- 🔒 **Security Professionals** - Comprehensive penetration testing
- 👨‍💻 **Developers** - Pre-deployment security checks
- 🏢 **Organizations** - Regular security assessments
- 🎓 **Students** - Learning security testing

### Why Choose VYOMA?

VYOMA combines traditional vulnerability scanning with cutting-edge AI technology to provide:

✅ **Intelligent Analysis** - AI-powered vulnerability detection using LLaMA 3.2
✅ **OWASP Coverage** - Complete OWASP Top 10 2021 testing
✅ **Multiple Modes** - Basic, Medium, and Aggressive scanning
✅ **Detailed Reports** - Beautiful HTML reports with risk scoring
✅ **Easy to Use** - Simple installation and intuitive interface
✅ **DevSecOps Integration** - Seamless CI/CD pipeline integration with security gates

---

## ✨ Key Features

### 🤖 AI-Powered Intelligence

- **LLaMA 3.2 Integration** - Advanced AI model for intelligent vulnerability analysis
- **Smart Payload Generation** - Context-aware exploit payloads
- **Chain Attack Detection** - Identifies multi-step exploitation paths
- **Risk Assessment** - AI-driven vulnerability prioritization
- **Executive Summaries** - Business impact analysis

### 🔍 Comprehensive Testing

**OWASP Top 10 2021 Coverage:**

| # | Category | Tests Included |
|---|----------|----------------|
| A01 | Broken Access Control | IDOR, Path Traversal, Privilege Escalation |
| A02 | Cryptographic Failures | Weak SSL/TLS, Insecure Protocols |
| A03 | Injection | SQL, NoSQL, Command, LDAP, XXE |
| A04 | Insecure Design | Business Logic Flaws |
| A05 | Security Misconfiguration | Default Credentials, Unnecessary Features |
| A06 | Vulnerable Components | Outdated Software Detection |
| A07 | Authentication Failures | Weak Passwords, Session Issues |
| A08 | Data Integrity Failures | Deserialization Attacks |
| A09 | Logging Failures | Security Event Analysis |
| A10 | SSRF | Server-Side Request Forgery |

### 🎨 Professional Interface

- **Modern GUI** - Burp Suite-inspired blue-gray theme
- **Real-time Monitoring** - Live vulnerability detection
- **Color-coded Severity** - Critical (Red), High (Orange), Medium (Yellow), Low (Blue)
- **Multiple Views** - Console, Vulnerabilities, Summary, AI Analysis
- **Export Options** - HTML and JSON reports

### 🔄 DevSecOps Integration

- **CI/CD Pipeline Integration** - Ready-to-use configurations for GitHub Actions, GitLab CI, and Jenkins
- **Security Gates** - Automated pipeline failures based on vulnerability thresholds
- **Shift-Left Security** - Catch vulnerabilities early in development cycle
- **Artifact Archiving** - Compliance reporting and review capabilities
- **Environment Configuration** - Easy setup through environment variables

---

## 💻 System Requirements

### Minimum Requirements

- **Operating System**: 
  - Windows 10/11
  - Linux: Ubuntu 20.04+, Kali Linux, Parrot OS, Debian, Fedora, Arch
  - macOS 11+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum
- **Storage**: 5GB free space
- **Internet**: Required for initial setup

### ✅ Tested On

VYOMA has been tested and works perfectly on:
- ✅ **Kali Linux** (2023.x and later)
- ✅ **Parrot Security OS** (5.x and later)
- ✅ **Ubuntu** (20.04, 22.04, 24.04)
- ✅ **Debian** (11, 12)
- ✅ **Windows** (10, 11)
- ✅ **macOS** (11+)

### Recommended Specifications

- **RAM**: 8GB or more
- **CPU**: Multi-core processor (4+ cores)
- **Storage**: 10GB free space
- **Internet**: Stable connection

---

## 🚀 Installation

### Quick Install (Recommended)

**Step 1: Clone the Repository**
```bash
git clone https://github.com/cahyod/vyoma.git
cd vyoma
```

**Step 2: Run the Installer**

**Windows:**
```bash
# Run the automated installer
install.bat
```

**Linux/macOS:**
```bash
# Make installer executable
chmod +x install.sh

# Run installer
./install.sh
```

The installer will automatically:
- ✅ Check Python 3.8+
- ✅ Install all dependencies
- ✅ Install Ollama + LLaMA 3.2:3b
- ✅ Create necessary directories
- ✅ Verify installation

### Manual Installation

**Step 1: Install Python**
- Download Python 3.8+ from [python.org](https://python.org)
- Make sure to check "Add Python to PATH"

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Install Ollama**

**Windows:**
- Download from [ollama.ai](https://ollama.ai)
- Run the installer

**Linux (Ubuntu/Debian/Kali/Parrot):**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Kali Linux / Parrot OS (Alternative):**
```bash
# If above doesn't work, use:
sudo apt update
sudo apt install curl
curl -fsSL https://ollama.ai/install.sh | sudo sh
```

**macOS:**
```bash
brew install ollama
```

**Step 4: Download AI Model**
```bash
ollama pull llama3.2:3b
```

**Step 5: Verify Installation**
```bash
python verify_installation.py
```

---

## 🎮 How to Run

### GUI Mode (Recommended)

**Launch Professional GUI:**
```bash
python vyoma_gui.py
```

Or use the main launcher:
```bash
python vyoma.py
```

**GUI Features:**
- 📊 Real-time vulnerability statistics
- 🔍 Live console output
- 📈 Interactive vulnerability tree
- 🤖 AI analysis dashboard

### CLI Mode

**Basic Commands:**
```bash
# Show help
python vyoma.py --help

# Basic scan (Fast)
python vyoma.py -u https://example.com --basic

# Medium scan (Standard)
python vyoma.py -u https://example.com

# Aggressive scan (Thorough)
python vyoma.py -u https://example.com --aggressive
```

**Advanced Commands:**
```bash
# Full OWASP testing
python main.py -u https://example.com --owasp-all

# Chain attack detection
python main.py -u https://example.com --chain-attacks

# Custom payloads
python main.py -u https://example.com --custom-payloads payloads.txt

# Verbose output with JSON report
python main.py -u https://example.com --verbose --format json
```

---

## 📊 Usage Examples

### Example 1: Quick Security Check

```bash
# Fast scan for quick assessment
python vyoma.py -u http://testphp.vulnweb.com/ --basic
```

**Use Case:** Quick initial assessment before detailed testing

### Example 2: Standard Security Assessment

```bash
# Medium scan with OWASP Top 10
python vyoma.py -u http://demo.testfire.net/
```

**Use Case:** Regular security testing and compliance checks

### Example 3: Thorough Security Audit

```bash
# Aggressive scan with all features
python vyoma.py -u https://example.com --aggressive --verbose
```

**Use Case:** Pre-production security audit and penetration testing

### Example 4: Custom Testing

```bash
# Advanced scan with custom payloads
python main.py -u https://example.com --owasp-all --chain-attacks \
               --custom-payloads payloads/custom.txt --threads 20
```

**Use Case:** Specialized testing with custom attack vectors

### Example 5: CI/CD Pipeline Integration

```bash
# Run security scan in CI/CD pipeline with thresholds
python vyoma_cicd_integration.py --target https://staging.example.com --mode basic --threshold-critical 0 --threshold-high 5

# Using environment variables
export VYOMA_TARGET_URL=https://staging.example.com
export VYOMA_THRESHOLD_CRITICAL=0
export VYOMA_THRESHOLD_HIGH=3
python vyoma_cicd_integration.py

# Initialize CI/CD configuration for GitHub Actions
python setup_cicd.py github --target-url https://example.com
```

**Use Case:** DevSecOps integration with security gates in deployment pipelines

### Test Targets (For Practice)

```bash
# Vulnerable PHP application
python vyoma.py -u http://testphp.vulnweb.com/

# Banking demo application
python vyoma.py -u http://demo.testfire.net/

# HTTP testing service
python vyoma.py -u https://httpbin.org/
```

---

## 🎯 Scan Modes

### ⚡ Basic Scan

**Duration:** Fast scan

**Features:**
- Fast vulnerability detection
- Common security issues
- OWASP Top 10: OFF by default
- Chain Attacks: Not available

**Best For:**
- Quick initial assessment
- Time-sensitive scans
- Basic security checks

**Command:**
```bash
python vyoma.py -u <URL> --basic
```

### 🔍 Medium Scan (Default)

**Duration:** Standard scan

**Features:**
- Comprehensive OWASP Top 10 testing
- AI-powered vulnerability analysis
- OWASP Top 10: ON by default
- Chain Attacks: Optional

**Best For:**
- Standard security assessment
- Regular testing
- Compliance checks

**Command:**
```bash
python vyoma.py -u <URL>
```

### 🔥 Aggressive Scan

**Duration:** Thorough scan

**Features:**
- Deep penetration testing
- AI chain attack detection
- OWASP Top 10: ON by default
- Chain Attacks: ON by default

**Best For:**
- Thorough security audit
- Pre-production testing
- Penetration testing

**Command:**
```bash
python vyoma.py -u <URL> --aggressive
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Python Not Found

**Problem:** `python: command not found`

**Solution:**
```bash
# Windows: Reinstall Python and check "Add to PATH"
# Linux/Mac: Install Python 3
sudo apt install python3  # Ubuntu/Debian
brew install python3      # macOS
```

#### Issue 2: Ollama Not Starting

**Problem:** Ollama service won't start

**Solution:**
```bash
# Start Ollama manually
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

#### Issue 3: LLaMA Model Not Found

**Problem:** Model download interrupted or missing

**Solution:**
```bash
# Download model again
ollama pull llama3.2:3b

# Verify installation
ollama list
```

#### Issue 4: Dependencies Installation Failed

**Problem:** pip install fails

**Solution:**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies again
pip install -r requirements.txt

# If specific package fails, install individually
pip install aiohttp requests dnspython beautifulsoup4
```

#### Issue 5: Permission Denied (Linux/Mac)

**Problem:** Permission errors during installation

**Solution:**
```bash
# Don't use sudo for the installer
# But you may need sudo for Ollama
curl -fsSL https://ollama.ai/install.sh | sudo sh
```

#### Issue 6: GUI Not Opening

**Problem:** GUI window doesn't appear

**Solution:**
```bash
# Check if tkinter is installed
python -c "import tkinter"

# If error, install tkinter
# Ubuntu/Debian:
sudo apt-get install python3-tk

# macOS: (usually included with Python)
brew install python-tk
```

#### Issue 7: Unicode/Encoding Errors

**Problem:** Character encoding errors in console

**Solution:**
```bash
# Set environment variable
# Windows:
set PYTHONIOENCODING=utf-8

# Linux/Mac:
export PYTHONIOENCODING=utf-8
```

#### Issue 8: Scan Hangs or Freezes

**Problem:** Scan stops responding

**Solution:**
- Reduce threads: `--threads 5`
- Increase timeout: `--timeout 60`
- Check internet connection
- Try basic scan first

### Verification

Run the verification script to check your installation:

```bash
python verify_installation.py
# or on some Linux systems:
python3 verify_installation.py
```

This will check:
- ✅ Python version
- ✅ All dependencies
- ✅ Ollama installation
- ✅ LLaMA model
- ✅ Project structure

### 🐧 Special Notes for Kali/Parrot Users

**Python Command:**
```bash
# Kali/Parrot usually use python3
python3 vyoma.py --help
python3 vyoma_gui.py
```

**If pip not found:**
```bash
sudo apt update
sudo apt install python3-pip
```

**If tkinter not found (for GUI):**
```bash
sudo apt install python3-tk
```

---

## �  Running on Kali Linux / Parrot OS

### Quick Start for Kali/Parrot Users

**1. Install Dependencies:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip (if not already installed)
sudo apt install python3 python3-pip python3-tk -y

# Install required packages
pip3 install -r requirements.txt
```

**2. Install Ollama:**
```bash
# Download and install Ollama
curl -fsSL https://ollama.ai/install.sh | sudo sh

# Start Ollama service
ollama serve &

# Download LLaMA model
ollama pull llama3.2:3b
```

**3. Run VYOMA:**
```bash
# Launch GUI
python3 vyoma_gui.py

# Or use CLI
python3 vyoma.py -u http://testphp.vulnweb.com/ --basic
```

### Kali/Parrot Specific Commands

**Check Python Version:**
```bash
python3 --version
# Should show Python 3.8 or higher
```

**Install Missing Dependencies:**
```bash
# If you get import errors
pip3 install aiohttp requests dnspython beautifulsoup4 lxml
```

**Run as Root (Not Recommended):**
```bash
# If you must run as root
sudo python3 vyoma.py -u <URL>
```

**Add to PATH (Optional):**
```bash
# Add alias to .bashrc or .zshrc
echo "alias vyoma='python3 ~/path/to/vyoma.py'" >> ~/.bashrc
source ~/.bashrc

# Now you can run:
vyoma -u <URL>
```

### Integration with Kali Tools

VYOMA works alongside other Kali tools:

```bash
# Use with nmap results
nmap -sV target.com -oX scan.xml
python3 vyoma.py -u http://target.com

# Use with nikto
nikto -h target.com
python3 vyoma.py -u http://target.com --aggressive

# Use with burpsuite
# Export targets from Burp and scan with VYOMA
python3 vyoma.py -u http://target.com --owasp-all
```

### Performance Tips for Kali/Parrot

**Optimize for VM:**
```bash
# If running in VM, reduce threads
python3 vyoma.py -u <URL> --threads 5

# Increase timeout for slow connections
python3 vyoma.py -u <URL> --timeout 60
```

**Save Resources:**
```bash
# Use basic scan for quick checks
python3 vyoma.py -u <URL> --basic

# Close other applications
# Allocate at least 4GB RAM to VM
```

---

## 📚 Help & Support

### Getting Help

**Command Line Help:**
```bash
# Main launcher help
python vyoma.py --help

# Advanced options help
python main.py --help

# Verify installation
python verify_installation.py
```



### Contact & Support

- 📧 **Email**: cahyod@yahoo.co.id
- 🐛 **Issues**: [GitHub Issues](https://github.com/cahyod/vyoma/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/cahyod/vyoma/discussions)

### Frequently Asked Questions

**Q: Is VYOMA free to use?**
A: Yes, VYOMA is open-source and free under MIT License.

**Q: Can I use it for commercial purposes?**
A: Yes, but only on systems you own or have permission to test.

**Q: Does it work on Windows?**
A: Yes, VYOMA supports Windows, Linux, and macOS.

**Q: How much does the AI model cost?**  
A: The LLaMA model is free and runs locally via Ollama.

**Q: Can I add custom payloads?**  
A: Yes, use `--custom-payloads` option with your payload file.

**Q: Is it safe to use?**  
A: Yes, but only use on authorized systems. Unauthorized scanning is illegal.

**Q: Does it work on Kali Linux?**  
A: Yes! VYOMA works perfectly on Kali Linux, Parrot OS, and all Debian-based distributions.

**Q: Can I run it in a VM?**
A: Yes, but allocate at least 4GB RAM and 10GB storage for best performance.

---

## ⚖️ Legal Notice

**⚠️ IMPORTANT: Authorized Use Only**

VYOMA is designed for authorized security testing and educational purposes only.

**Legal Requirements:**

✅ **DO:**
- Only scan systems you own
- Get explicit written permission before testing
- Use for educational purposes
- Follow responsible disclosure practices
- Comply with all applicable laws

❌ **DON'T:**
- Scan systems without permission
- Use for malicious purposes
- Violate computer crime laws
- Ignore terms of service
- Exploit vulnerabilities beyond proof-of-concept

**Disclaimer:**
- Users are responsible for complying with all applicable laws
- Unauthorized access to computer systems is illegal
- The developer assumes no liability for misuse
- This tool is provided "as is" without warranty

**Responsible Disclosure:**

If you discover vulnerabilities:
1. Do not exploit beyond proof-of-concept
2. Report to the system owner immediately
3. Allow reasonable time for fixes
4. Follow responsible disclosure practices

---

## 👨‍💻 Author

**Made with ❤️ by Cahyo Darujati**

**Developer:** Cahyo Darujati
**Email:** cahyod@yahoo.co.id
**GitHub:** [@cahyod](https://github.com/cahyod)

*Empowering security professionals with AI-driven vulnerability assessment*

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Ollama Team** - For the amazing AI runtime
- **Meta AI** - For LLaMA models
- **OWASP** - For security testing standards
- **Security Community** - For continuous feedback
- **Cybersecurity Indonesia** - For professional support and guidance

---

## **2-Year Feature Development Plan**

### **Phase 1: Core Enhancement (Months 1-6)**
- **Microservices Architecture**: Breaking down monolithic codebase into modular services
- **Plugin System**: Framework for adding new vulnerability detection methods
- **Advanced AI**: Integration of OpenAI, Anthropic, and local models
- **Performance Optimization**: Improved speed and resource efficiency
- **✅ DevSecOps Pipeline Integration**: Seamless integration with CI/CD platforms (GitHub Actions, GitLab CI, Jenkins) with security gates to prevent vulnerable code deployment

### **Phase 2: Advanced Features and Reporting (Months 4-10)**
- **Smart Attack Path Mapping**: Automated vulnerability chaining algorithms
- **Enterprise Reporting & Analytics**: Custom report templates and real-time dashboards
- **Threat Intelligence Integration**: Integration with external threat feeds
- **Automated Remediation Guidance**: Vulnerability repair guidance

### **Phase 3: Platform Expansion (Months 7-14)**
- **Cloud Security Assessment**: Support for AWS, Azure, GCP
- **DevSecOps Integration**: Enhanced CI/CD pipeline capabilities and platform support
- **Mobile Application Security**: Static and dynamic mobile app analysis
- **Container & Serverless Security**: Docker and Kubernetes security assessment

### **Phase 4: Advanced Intelligence & Operations (Months 10-18)**
- **Behavioral Analysis & Anomaly Detection**: Machine learning for threat detection
- **Automated Remediation Guidance**: Repair guidance based on vulnerabilities
- **Advanced Visualization & Collaboration**: Network mapping and workflow tools

### **Phase 5: Future Technologies (Months 15-24)**
- **Quantum-Resistant Assessment**: Evaluation for post-quantum cryptography readiness
- **IoT and Industrial Security**: IoT device security assessment modules
- **Predictive Security Analytics**: Predictive models for threat trends

### **Secure Code Checking Integration**
Static code analysis (SAST) feature will be added to analyze vulnerabilities in source code before deployment, supporting multiple programming languages and providing repair recommendations for developers.

### **DevSecOps Pipeline Integration - Implemented Feature**
VYOMA now includes comprehensive DevSecOps integration with:
- Ready-to-use configuration files for GitHub Actions, GitLab CI, and Jenkins
- Security gate functionality that can fail CI/CD pipelines based on vulnerability thresholds
- Easy setup through environment variables and configuration files
- Artifact archiving for compliance and review
- Support for multiple scan modes (basic, medium, aggressive)
- Shift-left security practices by catching vulnerabilities early in the development cycle

---

© 2025 Cahyo Darujati. All rights reserved.

**Version:** v1.0.0
**Last Updated:** November 2025
