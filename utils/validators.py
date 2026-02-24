"""
validators.py — File Validation and Security Scanning

Provides PDF file validation and malicious content detection.
Validates file extensions, magic numbers, and scans for suspicious PDF features.
"""

import os
from .logger import get_logger

logger = get_logger(__name__)


def is_pdf_file(file_path: str) -> bool:
    """
    Validate that a file is a genuine PDF using both extension and magic number.
    
    Checks:
    1. File has .pdf extension
    2. File starts with %PDF- magic number (PDF signature)
    
    Args:
        file_path: Path to the file to validate
    
    Returns:
        True if file is a valid PDF, False otherwise
    """
    # Check extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() != ".pdf":
        logger.debug(f"File rejected: incorrect extension '{ext}' for {file_path}")
        return False
    
    # Check magic number
    try:
        with open(file_path, "rb") as f:
            magic = f.read(5)
            is_valid = magic == b"%PDF-"
            
            if not is_valid:
                logger.warning(f"File rejected: invalid PDF magic number in {file_path}")
            else:
                logger.debug(f"File validated: {file_path}")
                
            return is_valid
    except Exception as e:
        logger.error(f"Validation error for {file_path}: {e}")
        return False


def scan_pdf_for_malicious_content(file_path: str) -> dict:
    """
    Scan PDF binary content for suspicious features that may indicate malware.
    
    Checks for common PDF-based attack vectors:
    - /JS, /JavaScript: Embedded JavaScript code
    - /AA, /OpenAction: Auto-run actions on document open
    - /Launch: Commands to launch external programs
    - /EmbeddedFile: Hidden embedded files
    - /AcroForm: Interactive forms (can execute scripts)
    - /RichMedia: Embedded media (Flash, video, etc.)
    
    Args:
        file_path: Path to the PDF file to scan
    
    Returns:
        Dictionary mapping suspicious keywords to occurrence counts
        Example: {"/JS": 2, "/JavaScript": 1, "/AA": 0, ...}
    """
    suspicious_keywords = {
        "/JS": 0,              # JavaScript in PDF
        "/JavaScript": 0,      # JavaScript object
        "/AA": 0,              # Auto-Action (triggers on open)
        "/OpenAction": 0,      # Action on document open
        "/Launch": 0,          # Launch external program
        "/EmbeddedFile": 0,    # Embedded files (can hide malware)
        "/AcroForm": 0,        # Interactive forms
        "/RichMedia": 0,       # Embedded media (Flash, etc.)
    }
    
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        
        # Count occurrences of each suspicious marker
        for keyword in suspicious_keywords:
            count = content.count(keyword.encode())
            suspicious_keywords[keyword] = count
        
        # Log findings
        found = {k: v for k, v in suspicious_keywords.items() if v > 0}
        if found:
            logger.warning(f"Suspicious elements detected in {file_path}: {found}")
        else:
            logger.info(f"Security scan passed: no threats in {file_path}")
            
    except Exception as e:
        logger.error(f"Malicious content scan error for {file_path}: {e}")
    
    return suspicious_keywords
