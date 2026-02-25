"""
workers.py — Background Worker Threads

Contains QThread worker classes for running long-running tasks
without blocking the GUI.
"""

import os
from typing import Any
from PyQt6.QtCore import QObject, pyqtSignal

from file_handlers.pdf_handler import extract_text_from_pdf
from analysis.ai_analysis import analyse_resume, AnalysisResult
from utils.html_helpers import (
    render_section_header,
    render_ok_line,
    render_warn_line,
    render_error_line,
    render_ai_analysis,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class AnalysisWorker(QObject):
    """
    Background worker for PDF analysis.
    
    Performs security scanning, text extraction, and AI analysis
    in a separate thread to avoid freezing the GUI.
    
    Signals:
        result: Emits HTML string with analysis results
        status: Emits status messages for the status bar
        analysis_ready: Emits the structured analysis dict
        finished: Emits when all work is complete
    """
    
    result = pyqtSignal(str)
    status = pyqtSignal(str)
    analysis_ready = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self, file_path: str, suspicious: dict[str, int]):
        """
        Initialize the analysis worker.
        
        Args:
            file_path: Path to the PDF file to analyze
            suspicious: Pre-scanned malicious content results
        """
        super().__init__()
        self.file_path = file_path
        self.suspicious = suspicious

    def run(self) -> None:
        """
        Execute the analysis workflow.
        
        Steps:
        1. Validate file still exists
        2. Display security scan results
        3. Extract text from PDF
        4. Run AI analysis on extracted text
        5. Emit results to GUI
        """
        fp = self.file_path
        name = os.path.basename(fp)
        html = ""

        try:
            # Guard: ensure file still exists before doing anything
            if not os.path.isfile(fp):
                logger.error(f"File not found: {fp}")
                self.result.emit(
                    render_error_line(f"✗ &nbsp; File no longer found: <b>{name}</b>") +
                    render_error_line("&nbsp;&nbsp;&nbsp;&nbsp;It may have been moved or deleted after selection.")
                )
                self.status.emit("● Error · File not found.")
                self.finished.emit()
                return

            # Security — use pre-scanned results from file selection
            self.status.emit("● Scanning · Checking for threats…")
            html += render_section_header("Security Scan", "#4fc3f7", "🔍")
            found = {k: v for k, v in self.suspicious.items() if v > 0}

            if found:
                html += render_warn_line(f"⚠ &nbsp; Suspicious elements detected in <b>{name}</b>:")
                for element, count in found.items():
                    html += render_warn_line(f"&nbsp;&nbsp;&nbsp;&nbsp;{element} &nbsp;·&nbsp; {count} occurrence(s)")
                html += render_warn_line("<br>Proceed with caution — file may contain active content.")
                logger.warning(f"Analyzing file with suspicious content: {fp}")
            else:
                html += render_ok_line(f"✓ &nbsp; No threats detected &nbsp;·&nbsp; {name} is clean")
                logger.info(f"Analyzing clean file: {fp}")

            # Extraction
            self.status.emit("● Extracting · Reading PDF…")
            logger.info(f"Extracting text from: {fp}")
            text = extract_text_from_pdf(fp)

            if not text:
                html += render_section_header("Extracted Text", "#c084fc", "📄")
                html += render_error_line("✗ &nbsp; No text could be extracted from this PDF.")
                html += render_error_line("&nbsp;&nbsp;&nbsp;&nbsp;The file may be image-only or encrypted.")
                logger.error(f"No text extracted from: {fp}")
            else:
                word_count = len(text.split())
                logger.info(f"Extracted {word_count} words from: {fp}")

                # AI Resume Analysis
                self.status.emit("● Analysing · Running AI resume review…")
                html += render_section_header("AI Resume Analysis", "#f9a825", "🤖")
                html += (
                    f'<p style="color:#4a5568; font-size:10px; margin:0 0 12px 2px; '
                    f'letter-spacing:0.5px;">📄 &nbsp; {word_count:,} words extracted &nbsp;·&nbsp; '
                    f'Analysed with llama3.1:8b</p>'
                )

                try:
                    logger.info(f"Starting AI analysis for: {fp}")
                    analysis: AnalysisResult = analyse_resume(text)
                    html += render_ai_analysis(analysis)
                    self.analysis_ready.emit(analysis)
                    logger.info(f"AI analysis completed successfully for: {fp}")
                except RuntimeError as ai_err:
                    html += render_error_line(f"✗ &nbsp; AI analysis failed: {ai_err}")
                    logger.error(f"AI analysis failed for {fp}: {ai_err}")

        except RuntimeError as e:
            html += render_error_line(f"✗ &nbsp; Could not read PDF: {e}")
            logger.error(f"PDF read error for {fp}: {e}")
        except Exception as e:
            html += render_error_line(f"✗ &nbsp; Unexpected error: {e}")
            logger.error(f"Unexpected error in worker for {fp}: {e}", exc_info=True)

        self.result.emit(html)
        self.status.emit("● Ready · Analysis complete.")
        logger.info(f"Analysis workflow completed for: {fp}")
        self.finished.emit()
