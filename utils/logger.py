"""
Logging utilities for Vyoma AI Security Scanner

This module provides centralized logging configuration with support for
console output, file logging, and optional colored output.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logger(name: str = "Vyoma_scanner", verbose: bool = False) -> logging.Logger:
    """Set up and configure a logger with console and file handlers.
    
    Args:
        name: Logger name (default: "Vyoma_scanner")
        verbose: If True, set log level to DEBUG; otherwise INFO
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Configure formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter('%(levelname)s: %(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler for detailed logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"Vyoma_scan_{timestamp}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Attempt to add colored output
    _setup_colored_logging(console_handler)
    
    logger.info("Logging initialized. Log file: %s", log_file)
    return logger


def _setup_colored_logging(handler: logging.Handler) -> None:
    """Attempt to configure colored logging if colorlog is available.
    
    Args:
        handler: The logging handler to configure with colors
    """
    try:
        import colorlog
        
        color_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)s%(reset)s: %(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        handler.setFormatter(color_formatter)
    except ImportError:
        pass  # colorlog not available, keep simple formatter
