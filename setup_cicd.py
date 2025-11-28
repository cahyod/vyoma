#!/usr/bin/env python3
"""
VYOMA CI/CD Integration Setup
Initializes CI/CD integration for various platforms
"""

import os
import sys
import argparse
from pathlib import Path
from vyoma_cicd_integration import CICDIntegration


def setup_github_actions():
    """Setup GitHub Actions workflow"""
    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: VYOMA Security Scan

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install Ollama
      run: |
        curl -fsSL https://ollama.ai/install.sh | sh &
        sleep 10  # Wait for Ollama to start

    - name: Pull LLaMA model
      run: |
        ollama pull llama3.2:3b

    - name: Install VYOMA dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run VYOMA security scan
      run: |
        python vyoma_cicd_integration.py --target ${{ secrets.TARGET_URL }} --mode basic --threshold-critical 0 --threshold-high 5

    - name: Archive security scan results
      uses: actions/upload-artifact@v3
      with:
        name: vyoma-scan-results
        path: reports/
"""
    
    workflow_file = workflow_dir / "vyoma-scan.yml"
    with open(workflow_file, 'w') as f:
        f.write(workflow_content)
    
    print(f"✅ GitHub Actions workflow created at {workflow_file}")


def setup_gitlab_ci():
    """Setup GitLab CI configuration"""
    gitlab_config = """stages:
  - security

variables:
  OLLAMA_HOST: 127.0.0.1:11434

before_script:
  - apt-get update && apt-get install -y curl
  - curl -fsSL https://ollama.ai/install.sh | sh &
  - sleep 10
  - ollama pull llama3.2:3b
  - pip install -r requirements.txt

vyoma-security-scan:
  stage: security
  image: python:3.11
  script:
    - echo "Starting VYOMA security scan..."
    - python vyoma_cicd_integration.py --target $CI_TARGET_URL --mode basic --threshold-critical 0 --threshold-high 5
    - echo "Security scan completed"
  artifacts:
    reports:
      sast: reports/vyoma-report.json
    paths:
      - reports/
    expire_in: 1 week
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
"""
    
    gitlab_file = Path(".gitlab-ci.yml")
    with open(gitlab_file, 'w') as f:
        f.write(gitlab_config)
    
    print(f"✅ GitLab CI configuration created at {gitlab_file}")


def setup_jenkins():
    """Setup Jenkins pipeline"""
    jenkins_content = """pipeline {
    agent any
    
    environment {
        OLLAMA_HOST = '127.0.0.1:11434'
    }
    
    stages {
        stage('Setup') {
            steps {
                script {
                    // Install Ollama
                    sh '''
                        if ! command -v ollama &> /dev/null; then
                            curl -fsSL https://ollama.ai/install.sh | sh
                        fi
                        nohup ollama serve > ollama.log 2>&1 &
                        sleep 15
                        ollama pull llama3.2:3b
                    '''
                }
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    sh 'python vyoma_cicd_integration.py --target ${TARGET_URL} --mode basic --threshold-critical 0 --threshold-high 5'
                }
            }
        }
        
        stage('Publish Results') {
            steps {
                script {
                    sh '''
                        if [ -f "reports/vyoma-report.json" ]; then
                            echo "Security scan completed. Results available in reports/"
                            cat reports/vyoma-report.json | jq '.vulnerabilities | length'
                        else
                            echo "No security report generated"
                            sh 'exit 1'
                        fi
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
                }
            }
        }
    }
    
    post {
        always {
            // Cleanup
            sh '''
                if pgrep -f "ollama serve"; then
                    pkill -f "ollama serve"
                fi
            '''
        }
    }
}
"""
    
    jenkins_file = Path("Jenkinsfile")
    with open(jenkins_file, 'w') as f:
        f.write(jenkins_content)
    
    print(f"✅ Jenkinsfile created at {jenkins_file}")


def main():
    parser = argparse.ArgumentParser(description="VYOMA CI/CD Integration Setup")
    parser.add_argument("platform", choices=['github', 'gitlab', 'jenkins', 'all'], 
                       help="CI/CD platform to setup")
    parser.add_argument("--target-url", required=True, 
                       help="Target URL to scan for security testing")
    
    args = parser.parse_args()
    
    # Set environment variable for target URL
    os.environ['VYOMA_TARGET_URL'] = args.target_url
    
    if args.platform in ['github', 'all']:
        setup_github_actions()
    
    if args.platform in ['gitlab', 'all']:
        setup_gitlab_ci()
    
    if args.platform in ['jenkins', 'all']:
        setup_jenkins()
    
    print("\n🎉 CI/CD integration setup complete!")
    print("\nNext steps:")
    print(f"1. Review the generated configuration files")
    print(f"2. Add required secrets/environment variables to your CI/CD platform")
    print(f"3. The target URL is set to: {args.target_url}")
    print(f"4. Default thresholds: 0 critical, 5 high vulnerabilities")
    print(f"5. Run 'python vyoma_cicd_integration.py --help' for more options")


if __name__ == "__main__":
    main()