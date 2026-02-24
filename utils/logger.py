"""
logger.py — Centralized Logging Configuration

Provides consistent logging setup for all modules in DocumentScannerAI.
Each module should call get_logger(__name__) to get its own logger.
"""

import logging
import os
from datetime import datetime


def setup_logging(log_file: str = "scanner.log", level: int = logging.INFO):
    """
    Configure the root logger for the entire application.
    
    Should be called once at application startup (in gui_main.py).
    
    Args:
        log_file: Path to the log file
        level: Logging level (default: logging.INFO)
    """
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Also log to console for development
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(
        logging.Formatter("%(levelname)s [%(name)s]: %(message)s")
    )
    logging.getLogger().addHandler(console)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name (typically __name__)
    
    Returns:
        Configured logger instance
    
    Example:
        logger = get_logger(__name__)
        logger.info("Processing started")
    """
    return logging.getLogger(name)
