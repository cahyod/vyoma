#!/usr/bin/env python3
"""
VYOMA CI/CD Integration Utilities
Provides functions to integrate VYOMA scanning into CI/CD pipelines
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class CICDIntegration:
    """Class to handle CI/CD pipeline integration"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize with optional config file"""
        self.config = self._load_config(config_file)
        
    def _load_config(self, config_file: Optional[str]) -> Dict:
        """Load configuration from file or use defaults"""
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "target_url": os.getenv("VYOMA_TARGET_URL", "http://localhost"),
                "scan_mode": os.getenv("VYOMA_SCAN_MODE", "basic"),
                "report_format": os.getenv("VYOMA_REPORT_FORMAT", "json"),
                "output_dir": os.getenv("VYOMA_OUTPUT_DIR", "./reports"),
                "threshold_critical": int(os.getenv("VYOMA_THRESHOLD_CRITICAL", "0")),
                "threshold_high": int(os.getenv("VYOMA_THRESHOLD_HIGH", "5"))
            }
    
    def run_security_scan(self) -> Dict:
        """Run VYOMA security scan in CI/CD environment"""
        try:
            # Build command based on configuration
            cmd = [
                sys.executable, "vyoma.py",
                "-u", self.config["target_url"],
                f"--{self.config['scan_mode']}",
                "--format", self.config["report_format"],
                "-o", self.config["output_dir"]
            ]
            
            if os.getenv("VYOMA_VERBOSE"):
                cmd.append("--verbose")
                
            print(f"Running security scan with command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            if result.returncode != 0:
                print(f"Scan failed with return code {result.returncode}")
                print(f"Error: {result.stderr}")
                return {"error": result.stderr, "returncode": result.returncode}
            
            # Parse results
            report_path = Path(self.config["output_dir"]) / f"vyoma_report_{self.config['target_url'].replace('http://', '').replace('https://', '').replace('.', '_')}_{Path(self.config['output_dir']).stat().st_mtime}.json"
            
            if report_path.exists():
                with open(report_path, 'r') as f:
                    scan_results = json.load(f)
                return scan_results
            else:
                return {"error": f"Report file not found at {report_path}"}
                
        except subprocess.TimeoutExpired:
            return {"error": "Scan timed out after 1 hour"}
        except Exception as e:
            return {"error": str(e)}
    
    def check_vulnerability_thresholds(self, scan_results: Dict) -> Dict:
        """Check if scan results exceed security thresholds"""
        if "error" in scan_results:
            return {"passed": False, "message": f"Scan failed: {scan_results['error']}"}
        
        vulnerabilities = scan_results.get("vulnerabilities", [])
        
        critical_count = sum(1 for v in vulnerabilities if v.get("severity", "").lower() == "critical")
        high_count = sum(1 for v in vulnerabilities if v.get("severity", "").lower() == "high")
        
        threshold_results = {
            "critical_count": critical_count,
            "high_count": high_count,
            "threshold_critical": self.config["threshold_critical"],
            "threshold_high": self.config["threshold_high"],
            "passed": True,
            "message": "Security scan passed thresholds"
        }
        
        if critical_count > self.config["threshold_critical"]:
            threshold_results["passed"] = False
            threshold_results["message"] = f"CRITICAL threshold exceeded: {critical_count} critical vulnerabilities found, threshold is {self.config['threshold_critical']}"
        elif high_count > self.config["threshold_high"]:
            threshold_results["passed"] = False
            threshold_results["message"] = f"HIGH threshold exceeded: {high_count} high vulnerabilities found, threshold is {self.config['threshold_high']}"
        
        return threshold_results
    
    def generate_security_gate(self) -> int:
        """Generate security gate result and return exit code"""
        print("Starting VYOMA security scan in CI/CD pipeline...")
        scan_results = self.run_security_scan()
        
        if "error" in scan_results:
            print(f"❌ Security scan failed: {scan_results['error']}")
            return 1
        
        print("✅ Security scan completed successfully")
        threshold_check = self.check_vulnerability_thresholds(scan_results)
        
        print(f"📊 Vulnerability Summary:")
        print(f"   Critical: {threshold_check['critical_count']} (threshold: {threshold_check['threshold_critical']})")
        print(f"   High: {threshold_check['high_count']} (threshold: {threshold_check['threshold_high']})")
        
        if threshold_check["passed"]:
            print(f"✅ {threshold_check['message']}")
            return 0
        else:
            print(f"❌ {threshold_check['message']}")
            return 1


def main():
    """Main function for CI/CD integration"""
    import argparse
    
    parser = argparse.ArgumentParser(description="VYOMA CI/CD Integration")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--target", help="Target URL to scan")
    parser.add_argument("--mode", help="Scan mode (basic, medium, aggressive)")
    parser.add_argument("--threshold-critical", type=int, help="Critical vulnerability threshold")
    parser.add_argument("--threshold-high", type=int, help="High vulnerability threshold")
    
    args = parser.parse_args()
    
    # Initialize integration
    integration = CICDIntegration(args.config)
    
    # Override config with command line arguments if provided
    if args.target:
        integration.config["target_url"] = args.target
    if args.mode:
        integration.config["scan_mode"] = args.mode
    if args.threshold_critical is not None:
        integration.config["threshold_critical"] = args.threshold_critical
    if args.threshold_high is not None:
        integration.config["threshold_high"] = args.threshold_high
    
    # Run security gate check
    exit_code = integration.generate_security_gate()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()