"""
main_window.py — Main Application Window

Contains the MainWindow class which defines the entire GUI layout,
event handlers, and application logic for DocumentScannerAI.
"""

import os
from typing import Any
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QFrame, QFileDialog, QMessageBox,
    QProgressBar
)
from PyQt6.QtCore import QThread, Qt
from fpdf import FPDF

from .workers import AnalysisWorker
from utils.validators import is_pdf_file, scan_pdf_for_malicious_content, check_file_size
from utils.logger import get_logger

logger = get_logger(__name__)


def _divider() -> QFrame:
    """Create a horizontal divider line."""
    line = QFrame()
    line.setObjectName("divider")
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    return line


class MainWindow(QMainWindow):
    """
    Main application window for DocumentScannerAI.
    
    Provides a two-panel interface:
    - Left sidebar: File selection and analysis controls
    - Right main area: Analysis results display
    """

    def __init__(self):
        """Initialize the main window and UI components."""
        super().__init__()
        self.setWindowTitle("DocumentScannerAI")
        self.setMinimumSize(960, 640)
        self.resize(1100, 720)
        
        # State variables
        self.selected_file: str | None = None
        self._last_scan: dict[str, int] = {}
        self._last_analysis: dict[str, Any] = {}
        self._thread: QThread | None = None
        self._worker: AnalysisWorker | None = None

        self._build_ui()
        logger.info("Main window initialized")

    def _build_ui(self) -> None:
        """Build the entire UI layout."""
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())
        root.addWidget(self._build_main())

        self.statusBar().setObjectName("statusBar")
        self.statusBar().showMessage("● Ready · No file selected")

    # ══════════════════════════════════════════════════════════════════════════
    # Sidebar
    # ══════════════════════════════════════════════════════════════════════════

    def _build_sidebar(self) -> QWidget:
        """Build the left sidebar with controls."""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(260)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo area
        logo_widget = QWidget()
        logo_widget.setObjectName("logoArea")
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setContentsMargins(24, 28, 24, 20)
        logo_layout.setSpacing(4)

        icon = QLabel("⬡")
        icon.setObjectName("appIcon")
        name = QLabel("DocumentScanner")
        name.setObjectName("appName")
        tagline = QLabel("AI-Powered Resume Analysis")
        tagline.setObjectName("appTagline")

        logo_layout.addWidget(icon)
        logo_layout.addWidget(name)
        logo_layout.addWidget(tagline)
        layout.addWidget(logo_widget)
        layout.addWidget(_divider())

        # File section
        file_widget = QWidget()
        file_widget.setObjectName("fileSection")
        file_layout = QVBoxLayout(file_widget)
        file_layout.setContentsMargins(20, 20, 20, 12)
        file_layout.setSpacing(10)

        doc_label = QLabel("DOCUMENT")
        doc_label.setObjectName("sectionLabel")

        self.selectButton = QPushButton("  Select PDF  ")
        self.selectButton.setObjectName("selectButton")
        self.selectButton.setMinimumHeight(40)
        self.selectButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.selectButton.setToolTip("Open a PDF file to analyse")
        self.selectButton.clicked.connect(self.select_pdf)

        # File info box
        file_info = QWidget()
        file_info.setObjectName("fileInfoBox")
        file_info_layout = QVBoxLayout(file_info)
        file_info_layout.setContentsMargins(12, 10, 12, 10)
        file_info_layout.setSpacing(3)

        file_header = QLabel("SELECTED FILE")
        file_header.setObjectName("fileLabelHeader")
        self.fileLabel = QLabel("No file selected")
        self.fileLabel.setObjectName("fileLabel")
        self.fileLabel.setWordWrap(True)

        file_info_layout.addWidget(file_header)
        file_info_layout.addWidget(self.fileLabel)

        file_layout.addWidget(doc_label)
        file_layout.addWidget(self.selectButton)
        file_layout.addWidget(file_info)
        layout.addWidget(file_widget)
        layout.addWidget(_divider())

        # Analyze section
        analyze_widget = QWidget()
        analyze_widget.setObjectName("analyzeSection")
        analyze_layout = QVBoxLayout(analyze_widget)
        analyze_layout.setContentsMargins(20, 16, 20, 16)
        analyze_layout.setSpacing(10)

        analyze_label = QLabel("ANALYSIS")
        analyze_label.setObjectName("analyzeLabel")

        self.analyzeButton = QPushButton("  Run Analysis  ")
        self.analyzeButton.setObjectName("analyzeButton")
        self.analyzeButton.setMinimumHeight(40)
        self.analyzeButton.setEnabled(False)
        self.analyzeButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.analyzeButton.setToolTip("Run security scan and text extraction")
        self.analyzeButton.clicked.connect(self.start_analysis)

        self.exportButton = QPushButton("  Export Report  ")
        self.exportButton.setObjectName("exportButton")
        self.exportButton.setMinimumHeight(40)
        self.exportButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exportButton.setToolTip("Save analysis results as a PDF report")
        self.exportButton.clicked.connect(self.export_report)
        self.exportButton.hide()

        analyze_layout.addWidget(analyze_label)
        analyze_layout.addWidget(self.analyzeButton)
        analyze_layout.addWidget(self.exportButton)
        layout.addWidget(analyze_widget)

        # Spacer
        layout.addStretch()
        layout.addWidget(_divider())

        # Footer
        footer = QWidget()
        footer.setObjectName("sidebarFooter")
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(20, 12, 20, 16)
        version = QLabel("v1.1.0  ·  MIT License")
        version.setObjectName("versionLabel")
        footer_layout.addWidget(version)
        layout.addWidget(footer)

        return sidebar

    # ══════════════════════════════════════════════════════════════════════════
    # Main content
    # ══════════════════════════════════════════════════════════════════════════

    def _build_main(self) -> QWidget:
        """Build the main content area with results display."""
        main = QWidget()
        main.setObjectName("mainContent")
        layout = QVBoxLayout(main)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top bar
        top_bar = QWidget()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(52)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(28, 0, 20, 0)

        page_title = QLabel("Analysis Results")
        page_title.setObjectName("pageTitle")

        self.statusDot = QLabel("● Ready")
        self.statusDot.setObjectName("statusDot")

        top_layout.addWidget(page_title)
        top_layout.addStretch()
        top_layout.addWidget(self.statusDot)

        # Results area
        self.resultsTextEdit = QTextEdit()
        self.resultsTextEdit.setObjectName("resultsTextEdit")
        self.resultsTextEdit.setReadOnly(True)
        self.resultsTextEdit.setPlaceholderText(
            "Select a PDF document and click Run Analysis to begin..."
        )
        self.resultsTextEdit.setFrameShape(QFrame.Shape.NoFrame)

        # Progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setObjectName("analysisProgress")
        self.progressBar.setTextVisible(False)
        self.progressBar.setRange(0, 1)
        self.progressBar.hide()

        layout.addWidget(top_bar)
        layout.addWidget(self.resultsTextEdit)
        layout.addWidget(self.progressBar)

        return main

    # ══════════════════════════════════════════════════════════════════════════
    # File selection
    # ══════════════════════════════════════════════════════════════════════════

    def select_pdf(self) -> None:
        """Handle PDF file selection."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a PDF Document", "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if not file_path:
            return

        logger.info(f"User selected file: {file_path}")

        # Check file size first
        size_ok, size_error = check_file_size(file_path)
        if not size_ok:
            QMessageBox.critical(
                self, "File Too Large",
                f"{size_error}\n\n"
                f"File: {os.path.basename(file_path)}\n\n"
                "Please select a smaller PDF file."
            )
            logger.warning(f"File rejected (size): {file_path}")
            return

        # Validate file
        if not is_pdf_file(file_path):
            QMessageBox.critical(
                self, "Invalid File",
                f"Not a valid PDF:\n\n{os.path.basename(file_path)}\n\n"
                "Please select a genuine PDF document."
            )
            logger.warning(f"Invalid PDF rejected: {file_path}")
            return

        # Scan for malicious content
        suspicious = scan_pdf_for_malicious_content(file_path)
        found = {k: v for k, v in suspicious.items() if v > 0}

        if found:
            details = "\n".join(f"  {k}: {v} occurrence(s)" for k, v in found.items())
            reply = QMessageBox.warning(
                self, "Suspicious File Detected",
                f"Potentially dangerous elements found:\n\n{details}\n\n"
                "This file may contain JavaScript or auto-run actions.\n\n"
                "Continue anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                self.statusBar().showMessage("File rejected.")
                logger.info(f"User rejected suspicious file: {file_path}")
                return

        # Accept file
        self.selected_file = file_path
        self._last_scan = suspicious
        self._last_analysis = {}
        self.fileLabel.setText(os.path.basename(file_path))
        self.analyzeButton.setEnabled(True)
        self.resultsTextEdit.clear()
        self.progressBar.hide()
        self.exportButton.hide()
        self.statusDot.setText("● Ready")
        self.statusBar().showMessage(f"Loaded: {os.path.basename(file_path)}")
        logger.info(f"File loaded successfully: {file_path}")

    # ══════════════════════════════════════════════════════════════════════════
    # Analysis
    # ══════════════════════════════════════════════════════════════════════════

    def start_analysis(self) -> None:
        """Start the analysis workflow in a background thread."""
        if not self.selected_file:
            return

        logger.info(f"Starting analysis for: {self.selected_file}")

        # Clean up previous thread if still running
        if self._thread is not None and self._thread.isRunning():
            logger.debug("Stopping previous analysis thread")
            self._thread.quit()
            self._thread.wait()
        self._thread = None
        self._worker = None

        # Prepare UI
        self.analyzeButton.setEnabled(False)
        self.selectButton.setEnabled(False)
        self.resultsTextEdit.clear()
        self.statusDot.setText("● Running")
        self.statusBar().showMessage("Analyzing…")
        
        # Show indeterminate progress
        self.progressBar.setRange(0, 0)
        self.progressBar.show()

        # Create worker thread
        self._thread = QThread()
        self._worker = AnalysisWorker(self.selected_file, self._last_scan)
        self._worker.moveToThread(self._thread)

        # Connect signals
        self._thread.started.connect(self._worker.run)
        self._worker.result.connect(self.resultsTextEdit.setHtml)
        self._worker.status.connect(self.statusBar().showMessage)
        self._worker.status.connect(self._update_dot)
        self._worker.analysis_ready.connect(self._store_analysis)
        self._worker.finished.connect(self._on_finished)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._reset_thread_refs)

        self._thread.start()
        logger.debug("Analysis thread started")

    def _update_dot(self, status: str) -> None:
        """Update the status dot based on status message."""
        if "Scanning" in status:
            self.statusDot.setText("● Scanning")
        elif "Extracting" in status:
            self.statusDot.setText("● Extracting")
        elif "Ready" in status:
            self.statusDot.setText("● Ready")

    def _on_finished(self) -> None:
        """Handle analysis completion."""
        # Hide progress bar
        self.progressBar.setRange(0, 1)
        self.progressBar.hide()
        
        # Re-enable buttons
        self.analyzeButton.setEnabled(True)
        self.selectButton.setEnabled(True)
        
        # Show export button if analysis succeeded
        if self._last_analysis:
            self.exportButton.show()
            logger.info("Analysis completed successfully")
        else:
            logger.info("Analysis completed without results")

    def _store_analysis(self, analysis: dict[str, Any]) -> None:
        """Store analysis results for export."""
        self._last_analysis = analysis
        logger.debug("Analysis results stored")

    def _reset_thread_refs(self) -> None:
        """Clean up thread references."""
        self._thread = None
        self._worker = None
        logger.debug("Thread references reset")

    # ══════════════════════════════════════════════════════════════════════════
    # Export
    # ══════════════════════════════════════════════════════════════════════════

    def export_report(self) -> None:
        """Export analysis results to a formatted PDF report."""
        if not self._last_analysis or not self.resultsTextEdit.toPlainText():
            logger.warning("Export attempted with no analysis results")
            return

        logger.info("Starting report export")

        # Open save dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Analysis Report", "Resume_Analysis_Report.pdf",
            "PDF Files (*.pdf)"
        )
        if not file_path:
            logger.info("Export cancelled by user")
            return

        logger.info(f"Exporting report to: {file_path}")

        # Disable button during generation
        self.exportButton.setEnabled(False)

        try:
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_margins(left=15, top=10, right=15)
            pdf.set_auto_page_break(auto=True, margin=15)

            # Header section
            pdf.set_fill_color(15, 17, 23)
            pdf.rect(0, 0, 210, 40, 'F')
            
            pdf.set_y(12)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 8, "RESUME ANALYSIS REPORT", 0, 1, 'C')
            
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(148, 163, 184)
            pdf.cell(0, 5, "Generated by DocumentScannerAI", 0, 1, 'C')
            
            pdf.set_text_color(110, 231, 183)
            filename_text = f"File: {os.path.basename(self.selected_file) if self.selected_file else 'Unknown'}"
            pdf.cell(0, 5, filename_text, 0, 1, 'C')
            
            pdf.set_y(45)
            pdf.set_left_margin(15)
            pdf.set_x(15)

            # Helper function for sections
            def add_section(title: str, content: list[str] | str) -> None:
                pdf.set_fill_color(26, 32, 53)
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(255, 255, 255)
                pdf.set_x(15)
                pdf.cell(0, 8, f"  {title}", 0, 1, 'L', True)
                
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(148, 163, 184)
                pdf.ln(2)
                
                pdf.set_x(15)
                if isinstance(content, list):
                    for item in content:
                        pdf.set_x(15)
                        item_text = str(item)
                        pdf.multi_cell(0, 5, f"> {item_text}")
                else:
                    pdf.multi_cell(0, 5, str(content))
                
                pdf.ln(3)

            # Add sections from analysis
            if "overall_impression" in self._last_analysis:
                add_section("OVERALL IMPRESSION", self._last_analysis["overall_impression"])
            
            if "strengths" in self._last_analysis:
                add_section("STRENGTHS", self._last_analysis["strengths"])
            
            if "weaknesses" in self._last_analysis:
                add_section("AREAS TO IMPROVE", self._last_analysis["weaknesses"])
            
            if "key_skills" in self._last_analysis:
                add_section("KEY SKILLS DETECTED", self._last_analysis["key_skills"])
            
            if "recommendations" in self._last_analysis:
                add_section("RECOMMENDATIONS", self._last_analysis["recommendations"])

            # Save PDF
            pdf.output(file_path)

            QMessageBox.information(
                self, "Report Exported",
                f"Report saved to:\n\n{file_path}"
            )
            logger.info(f"Report exported successfully to: {file_path}")

        except Exception as e:
            QMessageBox.critical(
                self, "Export Failed",
                f"Failed to export report:\n\n{str(e)}"
            )
            logger.error(f"Export error: {e}", exc_info=True)
        
        finally:
            # Re-enable button
            self.exportButton.setEnabled(True)
