#!/usr/bin/env python3
"""
Optimum Vyoma AI Security Scanner
Specially optimized for VPS with 4 CPU Cores and 8GB RAM

This version balances speed and thoroughness by:
- Using optimal thread count (16 threads for 4 cores)
- Aggressive connection pooling
- Optimized timeouts
- Smart AI analysis (only critical vulnerabilities)
- Efficient memory management
- Parallel task execution where possible
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.scanner_engine import VyomaAIScanner
from core.config import Config
from utils.logger import setup_logger
from utils.banner import display_banner
from utils.ollama_manager import OllamaManager

async def optimum_scan(target_url: str, fast_mode: bool = False):
    """Run an optimized scan for 4-core/8GB VPS"""
    
    display_banner()
    
    print("OPTIMUM Vyoma AI SECURITY SCANNER")
    print("=" * 70)
    print(f"Target: {target_url}")
    if fast_mode:
        print("Mode: FAST - Quick security assessment")
    else:
        print("Mode: BALANCED - Optimal speed vs thoroughness")
    print("Hardware Profile: 4 CPU Cores, 8GB RAM")
    print("=" * 70)
    print()
    
    # Initialize Ollama automatically
    print("Initializing AI Engine...")
    ollama_manager = OllamaManager()
    success, message = ollama_manager.initialize(auto_download=True)
    if success:
        print(f"✓ {message}")
    else:
        print(f"⚠ {message}")
        print("  Continuing without AI features...")
    print()
    
    # OPTIMAL CONFIGURATION FOR 4 CORE / 8GB RAM
    # Thread count: 4 cores * 4 = 16 threads (optimal for I/O bound tasks)
    # Timeout: 20s (balanced between speed and reliability)
    # Crawl depth: 2 (good coverage without excessive crawling)
    
    logger = setup_logger("optimum_scan", verbose=True)
    
    if fast_mode:
        # FAST MODE: Quick assessment
        config = Config(
            target_url=target_url,
            owasp_all=False,  # Skip comprehensive OWASP testing
            chain_attacks=False,  # Skip chain attacks
            model="llama3.2:3b",  # Lightweight model
            max_threads=12,  # Still aggressive but conservative
            timeout=15,  # Faster timeout
            output_dir="./optimum_scan_results",
            skip_port_scan=True,  # Skip port scanning
            max_crawl_depth=1  # Minimal crawling
        )
        scan_features = [
            "✓ Core vulnerability detection",
            "✓ Basic web crawling (depth: 1)",
            "✓ Essential security checks",
            "✓ Professional HTML reports",
            "✓ Minimal AI overhead",
            "✗ NO OWASP Top 10 testing",
            "✗ NO Port scanning",
            "✗ NO Chain attack analysis"
        ]
    else:
        # BALANCED MODE: Optimal thoroughness vs speed
        config = Config(
            target_url=target_url,
            owasp_all=True,  # Include OWASP testing
            chain_attacks=False,  # Skip chain attacks for speed
            model="llama3.2:3b",  # Lightweight model for speed
            max_threads=16,  # 4 cores * 4 = optimal for I/O
            timeout=20,  # Balanced timeout
            output_dir="./optimum_scan_results",
            skip_port_scan=False,  # Include port scanning
            max_crawl_depth=2  # Moderate crawling depth
        )
        scan_features = [
            "✓ Comprehensive vulnerability detection",
            "✓ Web crawling (depth: 2)",
            "✓ OWASP Top 10 testing",
            "✓ Port scanning & service detection",
            "✓ Professional HTML reports",
            "✓ Optimized AI analysis",
            "✗ NO Chain attack analysis (for speed)"
        ]
    
    try:
        # Initialize scanner
        scanner = VyomaAIScanner(config, logger)
        
        print("STARTING OPTIMUM SCAN...")
        print("=" * 70)
        print("SCAN FEATURES:")
        for feature in scan_features:
            print(f"   {feature}")
        print("=" * 70)
        print()
        
        # Enable optimized AI analysis (skip detailed analysis for speed)
        scanner.skip_ai_analysis = fast_mode
        
        # Run the scan
        results = await scanner.run_full_scan()
        
        # Display results
        print("\n" + "=" * 70)
        print("OPTIMUM SCAN COMPLETED!")
        print("=" * 70)
        print(f"Target: {results['target']}")
        print(f"Risk Score: {results.get('risk_score', 0)}/100")
        print(f"Total Vulnerabilities: {len(results.get('vulnerabilities', []))}")
        print(f"Report: {results.get('report_path', 'Not generated')}")
        print(f"Duration: {results.get('scan_duration', 0):.2f} seconds ({results.get('scan_duration', 0)/60:.2f} minutes)")
        
        # Show vulnerability summary
        vulnerabilities = results.get('vulnerabilities', [])
        if vulnerabilities:
            print(f"\nVULNERABILITY SUMMARY:")
            vuln_types = {}
            severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Info': 0}
            
            for vuln in vulnerabilities:
                vuln_type = vuln.get('type', 'Unknown')
                vuln_types[vuln_type] = vuln_types.get(vuln_type, 0) + 1
                
                severity = vuln.get('severity', 'Info')
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            print("\nBy Severity:")
            for severity, count in severity_counts.items():
                if count > 0:
                    print(f"   {severity}: {count}")
            
            print("\nBy Type:")
            for vuln_type, count in sorted(vuln_types.items(), key=lambda x: x[1], reverse=True):
                print(f"   {vuln_type}: {count}")
            
            print(f"\nTOP 5 CRITICAL VULNERABILITIES:")
            high_priority = [v for v in vulnerabilities if v.get('severity') in ['Critical', 'High']]
            for i, vuln in enumerate(high_priority[:5], 1):
                print(f"   {i}. {vuln.get('type', 'Unknown')} [{vuln.get('severity', 'N/A')}]")
                print(f"      URL: {vuln.get('url', 'N/A')}")
                print(f"      Parameter: {vuln.get('parameter', 'N/A')}")
                print()
        
        print(f"\nPERFORMANCE METRICS:")
        print(f"   Threads Used: {config.max_threads}")
        print(f"   Timeout: {config.timeout}s")
        print(f"   Crawl Depth: {config.max_crawl_depth}")
        print(f"   OWASP Testing: {'Enabled' if config.owasp_all else 'Disabled'}")
        print(f"   Port Scanning: {'Enabled' if not config.skip_port_scan else 'Disabled'}")
        
        print(f"\nRECOMMENDATIONS:")
        if results.get('risk_score', 0) >= 75:
            print("   ⚠️  HIGH RISK - Immediate action required!")
        elif results.get('risk_score', 0) >= 50:
            print("   ⚡ MEDIUM RISK - Schedule remediation soon")
        else:
            print("   ✓ LOW RISK - Continue monitoring")
        
        if fast_mode:
            print("\n💡 TIP: For more thorough scanning, run without --fast flag")
        
        return results
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        return None
    except Exception as e:
        print(f"\nScan failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Optimum Vyoma AI Security Scanner for 4-Core/8GB VPS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python optimum_scan.py -u https://example.com
  python optimum_scan.py -u https://example.com --fast
  python optimum_scan.py -u https://example.com --output ./reports

Modes:
  Default (Balanced): Optimal mix of speed and thoroughness
                      - 16 threads, 20s timeout, crawl depth 2
                      - Includes OWASP testing and port scanning
                      - Estimated time: 5-15 minutes
  
  Fast Mode (--fast): Quick security assessment
                      - 12 threads, 15s timeout, crawl depth 1
                      - Skips OWASP testing and port scanning
                      - Estimated time: 1-3 minutes

Hardware Optimization:
  This scanner is optimized for VPS with:
  - 4 CPU Cores
  - 8GB RAM
  - SSD Storage (recommended)
  
  Thread calculation: CPU cores × 4 = 16 threads (I/O bound optimal)
        """
    )
    parser.add_argument('-u', '--url', required=True, help='Target URL to scan')
    parser.add_argument('--fast', action='store_true', help='Enable fast mode (quicker, less thorough)')
    parser.add_argument('-o', '--output', default='./optimum_scan_results', help='Output directory for reports')
    
    args = parser.parse_args()
    
    # Update output directory if specified
    if args.output:
        import os
        os.makedirs(args.output, exist_ok=True)
    
    # Run optimum scan
    asyncio.run(optimum_scan(args.url, fast_mode=args.fast))

if __name__ == "__main__":
    main()
