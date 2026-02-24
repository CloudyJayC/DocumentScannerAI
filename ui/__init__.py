"""
ui — User Interface Components for DocumentScannerAI

This package contains all PyQt6 GUI components:
- styles: Application-wide stylesheet
- workers: Background worker threads
- main_window: Main application window
"""

from .styles import APP_STYLE
from .workers import AnalysisWorker
from .main_window import MainWindow

__all__ = ["APP_STYLE", "AnalysisWorker", "MainWindow"]
