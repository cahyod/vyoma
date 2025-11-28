# VYOMA CI/CD Integration Guide

This document provides instructions for integrating VYOMA security scanning into popular CI/CD platforms.

## Overview

VYOMA provides seamless integration with the following CI/CD platforms:
- GitHub Actions
- GitLab CI
- Jenkins
- Azure DevOps (Coming Soon)
- CircleCI (Coming Soon)

## GitHub Actions Integration

### Setup
1. Copy the `github-actions.yml` file to `.github/workflows/vyoma-scan.yml` in your repository
2. Add the following secrets to your GitHub repository:
   - `TARGET_URL`: The URL to scan
3. The workflow will automatically trigger on push and pull requests

### Configuration
You can customize the scan by modifying:
- Scan mode (`--basic`, `--medium`, `--aggressive`)
- Target URL
- Report format
- Vulnerability thresholds

## GitLab CI Integration

### Setup
1. Copy the content from `gitlab-ci.yml` to your `.gitlab-ci.yml` file
2. Set the `CI_TARGET_URL` variable in your GitLab CI/CD settings
3. The pipeline job will run during security stage

### Configuration
- Adjust the threshold values in the CI variables
- Modify the scan parameters as needed
- Configure artifact retention policy

## Jenkins Integration

### Setup
1. Use the provided `jenkinsfile` as your Jenkins Pipeline script
2. Set environment variables in your Jenkins job:
   - `TARGET_URL`: The URL to scan
3. The pipeline will run through setup, security scan, and publish stages

### Configuration
- Modify the pipeline stages as needed
- Adjust timeout values for longer scans
- Configure notification settings

## Standalone CLI Usage

### Basic Usage
```bash
python vyoma_cicd_integration.py --target https://example.com --mode basic
```

### Advanced Usage
```bash
python vyoma_cicd_integration.py \
  --config cicd_config.json \
  --threshold-critical 0 \
  --threshold-high 5
```

### Environment Variables
You can configure the integration using these environment variables:

- `VYOMA_TARGET_URL`: Target URL to scan (default: http://localhost)
- `VYOMA_SCAN_MODE`: Scan mode (basic, medium, aggressive) (default: basic)
- `VYOMA_REPORT_FORMAT`: Report format (json, html) (default: json)
- `VYOMA_OUTPUT_DIR`: Output directory for reports (default: ./reports)
- `VYOMA_THRESHOLD_CRITICAL`: Critical vulnerability threshold (default: 0)
- `VYOMA_THRESHOLD_HIGH`: High vulnerability threshold (default: 5)
- `VYOMA_VERBOSE`: Enable verbose output (default: false)

## Configuration File Format

You can create a JSON configuration file to define all settings:

```json
{
  "target_url": "https://example.com",
  "scan_mode": "basic",
  "report_format": "json",
  "output_dir": "./reports",
  "threshold_critical": 0,
  "threshold_high": 5
}
```

## Security Gate Behavior

The CI/CD integration includes security gates that will:
1. Pass the pipeline if vulnerability counts are within thresholds
2. Fail the pipeline if thresholds are exceeded
3. Generate detailed reports for review
4. Archive scan results for compliance

## Exit Codes

- `0`: Security scan passed all thresholds
- `1`: Security scan failed or exceeded thresholds
- `2`: Configuration error
- `3`: Scan execution error

## Examples

### GitHub Actions with Custom Thresholds
```yaml
- name: Run VYOMA security scan
  run: |
    python vyoma_cicd_integration.py --target ${{ secrets.TARGET_URL }} --threshold-critical 0 --threshold-high 10
```

### GitLab CI with Multiple Targets
```yaml
variables:
  TARGET_URL: "https://staging.example.com"
  
before_script:
  - pip install -r requirements.txt
  
staging-security-scan:
  script:
    - python vyoma_cicd_integration.py --target $TARGET_URL
```

## Troubleshooting

### Common Issues
1. **Ollama not found**: Ensure Ollama is installed and running in your CI environment
2. **Permission denied**: Check file permissions for reports directory
3. **Timeout errors**: Increase timeout values for large applications

### Debug Mode
Add `--verbose` flag or set `VYOMA_VERBOSE=true` for detailed logging.