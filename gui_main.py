"""
gui_main.py — DocumentScannerAI GUI Entry Point
================================================

A professional dark-themed GUI for PDF scanning and AI-powered resume analysis.
Features file validation, malicious content detection, text extraction, and
structured AI analysis using a local Ollama instance (llama3.1:8b model).

Run with: python gui_main.py
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication

from ui import APP_STYLE, MainWindow
from utils.logger import setup_logging
from config import LOG_FILE, LOG_LEVEL


def main():
    """Main entry point for the application."""
    # Setup logging first
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    setup_logging(log_file=LOG_FILE, level=log_level)
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLE)

    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

