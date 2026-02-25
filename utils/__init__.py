"""
utils — Shared Utilities for DocumentScannerAI

This package contains shared utility functions used across the application:
- logger: Centralized logging configuration
- validators: File validation and security scanning
- html_helpers: HTML rendering utilities for the GUI
"""

from .logger import get_logger
from .validators import is_pdf_file, scan_pdf_for_malicious_content, check_file_size
from .html_helpers import (
    render_section_header,
    render_ok_line,
    render_warn_line,
    render_error_line,
    render_ai_analysis,
    render_text_block,
)

__all__ = [
    "get_logger",
    "is_pdf_file",
    "check_file_size",
    "scan_pdf_for_malicious_content",
    "render_section_header",
    "render_ok_line",
    "render_warn_line",
    "render_error_line",
    "render_ai_analysis",
    "render_text_block",
]
