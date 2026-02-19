"""
gui_main.py — DocumentScannerAI GUI Entry Point (PyQt6)
========================================================
UI built entirely in Python — no .ui file required.
Run with: python gui_main.py
"""

import sys
import os
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QFrame, QFileDialog, QMessageBox,
    QStatusBar, QSizePolicy
)
from PyQt6.QtCore import QThread, pyqtSignal, QObject, Qt
from PyQt6.QtGui import QFont

from file_handlers.pdf_handler import extract_text_from_pdf

logging.basicConfig(
    filename="scanner.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# ══════════════════════════════════════════════════════════════════════════════
# Stylesheet
# ══════════════════════════════════════════════════════════════════════════════

APP_STYLE = """
QMainWindow, QWidget {
    background-color: #0f1117;
    color: #e2e8f0;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
    border: none;
}

QWidget#sidebar {
    background-color: #0a0d14;
    border-right: 1px solid #1e2433;
}

QLabel#appIcon {
    color: #6ee7f7;
    font-size: 26px;
}
QLabel#appName {
    color: #f0f6ff;
    font-size: 15px;
    font-weight: 700;
}
QLabel#appTagline {
    color: #374151;
    font-size: 10px;
}
QLabel#sectionLabel, QLabel#analyzeLabel {
    color: #2d3748;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
}
QLabel#fileLabelHeader {
    color: #2d3f5a;
    font-size: 8px;
    font-weight: 700;
    letter-spacing: 2px;
}
QLabel#fileLabel {
    color: #7dd3fc;
    font-size: 11px;
}
QLabel#versionLabel {
    color: #1f2d42;
    font-size: 10px;
}
QLabel#pageTitle {
    color: #cbd5e1;
    font-size: 13px;
    font-weight: 600;
}
QLabel#statusDot {
    color: #374151;
    font-size: 11px;
}

QWidget#fileInfoBox {
    background-color: #0d1120;
    border: 1px solid #1e2433;
    border-radius: 6px;
}

QFrame#divider {
    color: #1e2433;
    background-color: #1e2433;
    max-height: 1px;
    border: none;
}

QWidget#topBar {
    background-color: #0c0f1a;
    border-bottom: 1px solid #1e2433;
}

QPushButton#selectButton {
    background-color: #1a2035;
    color: #93c5fd;
    border: 1px solid #2a3654;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 600;
    text-align: left;
}
QPushButton#selectButton:hover {
    background-color: #1e2a45;
    border-color: #3b82f6;
    color: #bfdbfe;
}
QPushButton#selectButton:pressed {
    background-color: #172038;
}

QPushButton#analyzeButton {
    background-color: #1a3a2a;
    color: #6ee7b7;
    border: 1px solid #2a5a40;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 600;
    text-align: left;
}
QPushButton#analyzeButton:hover {
    background-color: #1e4a35;
    border-color: #10b981;
    color: #a7f3d0;
}
QPushButton#analyzeButton:pressed {
    background-color: #163028;
}
QPushButton#analyzeButton:disabled {
    background-color: #111820;
    color: #2d3748;
    border-color: #1a2030;
}

QTextEdit#resultsTextEdit {
    background-color: #0f1117;
    color: #cbd5e1;
    border: none;
    padding: 24px 32px;
    font-family: "Cascadia Code", "Fira Code", "Consolas", monospace;
    font-size: 12px;
    selection-background-color: #1e3a5f;
}

QScrollBar:vertical {
    background: #0a0d14;
    width: 6px;
    border: none;
}
QScrollBar::handle:vertical {
    background: #1e2a3d;
    border-radius: 3px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #2a3d5a;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QStatusBar {
    background-color: #080b11;
    color: #374151;
    font-size: 10px;
    border-top: 1px solid #111825;
    padding: 0 12px;
}

QMessageBox {
    background-color: #0f1117;
    color: #e2e8f0;
}
QMessageBox QPushButton {
    background-color: #1a2035;
    color: #93c5fd;
    border: 1px solid #2a3654;
    border-radius: 5px;
    padding: 6px 18px;
    min-width: 70px;
}
QMessageBox QPushButton:hover {
    background-color: #1e2a45;
    border-color: #3b82f6;
}
"""

# ══════════════════════════════════════════════════════════════════════════════
# Validation
# ══════════════════════════════════════════════════════════════════════════════

ALLOWED_EXTENSIONS = {".pdf"}


def is_pdf_file(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return False
    try:
        with open(file_path, "rb") as f:
            return f.read(5) == b"%PDF-"
    except Exception as e:
        logging.error(f"Validation error: {e}")
        return False


def scan_pdf_for_malicious_content(file_path: str) -> dict:
    suspicious_keywords = {
        "/JS": 0, "/JavaScript": 0, "/AA": 0, "/OpenAction": 0,
        "/Launch": 0, "/EmbeddedFile": 0, "/AcroForm": 0, "/RichMedia": 0,
    }
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        for keyword in suspicious_keywords:
            suspicious_keywords[keyword] = content.count(keyword.encode())
    except Exception as e:
        logging.error(f"Malicious scan error: {e}")
    return suspicious_keywords


# ══════════════════════════════════════════════════════════════════════════════
# HTML helpers
# ══════════════════════════════════════════════════════════════════════════════

def _section_header(title: str, color: str, icon: str = "") -> str:
    return (
        f'<div style="margin-top:28px; margin-bottom:10px;">'
        f'<span style="color:{color}; font-size:9px; font-weight:700; '
        f'letter-spacing:2.5px; font-family:Segoe UI,sans-serif;">'
        f'{icon}&nbsp;&nbsp;{title.upper()}'
        f'</span>'
        f'<hr style="border:none; border-top:1px solid #1a2236; margin-top:6px; margin-bottom:0;">'
        f'</div>'
    )


def _ok_line(text: str) -> str:
    return f'<p style="color:#6ee7b7; font-size:11px; margin:4px 0 0 2px;">{text}</p>'


def _warn_line(text: str) -> str:
    return f'<p style="color:#fbbf24; font-size:11px; margin:3px 0 0 2px;">{text}</p>'


def _error_line(text: str) -> str:
    return f'<p style="color:#f87171; font-size:11px; font-weight:600; margin:3px 0 0 2px;">{text}</p>'


def _coming_soon(label: str) -> str:
    return (
        f'<p style="color:#1f2d42; font-style:italic; font-size:11px; margin:6px 0 0 2px;">'
        f'[ {label} — coming in next patch ]</p>'
    )


def _text_block(text: str) -> str:
    escaped = (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    lines_html = []
    for line in escaped.split("\n"):
        stripped = line.strip()
        if not stripped:
            lines_html.append("<br>")
        elif stripped.isupper() and len(stripped) < 40:
            lines_html.append(
                f'<span style="color:#7dd3fc; font-weight:700; font-size:11px;">{line}</span><br>'
            )
        else:
            lines_html.append(f"{line}<br>")
    return (
        '<p style="font-family:Cascadia Code,Fira Code,Consolas,monospace; '
        'font-size:11.5px; color:#94a3b8; line-height:1.75; margin:6px 0 0 2px;">'
        + "".join(lines_html)
        + "</p>"
    )


# ══════════════════════════════════════════════════════════════════════════════
# Worker
# ══════════════════════════════════════════════════════════════════════════════

class AnalysisWorker(QObject):
    result   = pyqtSignal(str)
    status   = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, file_path: str, suspicious: dict):
        super().__init__()
        self.file_path = file_path
        self.suspicious = suspicious  # pre-scanned on file select, avoids double scan

    def run(self):
        fp = self.file_path
        name = os.path.basename(fp)
        html = ""

        try:
            # Guard: ensure file still exists before doing anything
            if not os.path.isfile(fp):
                self.result.emit(
                    _error_line(f"✗ &nbsp; File no longer found: <b>{name}</b>") +
                    _error_line("&nbsp;&nbsp;&nbsp;&nbsp;It may have been moved or deleted after selection.")
                )
                self.status.emit("● Error · File not found.")
                self.finished.emit()
                return

            # Security — use pre-scanned results from file selection
            self.status.emit("● Scanning · Checking for threats…")
            html += _section_header("Security Scan", "#4fc3f7", "🔍")
            found = {k: v for k, v in self.suspicious.items() if v > 0}

            if found:
                html += _warn_line(f"⚠ &nbsp; Suspicious elements detected in <b>{name}</b>:")
                for element, count in found.items():
                    html += _warn_line(f"&nbsp;&nbsp;&nbsp;&nbsp;{element} &nbsp;·&nbsp; {count} occurrence(s)")
                html += _warn_line("<br>Proceed with caution — file may contain active content.")
                logging.warning(f"Suspicious elements in {fp}: {found}")
            else:
                html += _ok_line(f"✓ &nbsp; No threats detected &nbsp;·&nbsp; {name} is clean")
                logging.info(f"Clean file: {fp}")

            # Extraction
            self.status.emit("● Extracting · Reading PDF…")
            html += _section_header("Extracted Text", "#c084fc", "📄")
            text = extract_text_from_pdf(fp)

            if not text:
                html += _error_line("✗ &nbsp; No text could be extracted from this PDF.")
                html += _error_line("&nbsp;&nbsp;&nbsp;&nbsp;The file may be image-only or encrypted.")
                logging.error(f"No text extracted: {fp}")
            else:
                word_count = len(text.split())
                html += (
                    f'<p style="color:#374151; font-size:10px; margin:0 0 8px 2px; '
                    f'letter-spacing:0.5px;">{word_count:,} words extracted</p>'
                )
                html += _text_block(text)
                logging.info(f"Text extracted: {fp}")

            # AI placeholder
            html += _section_header("AI Resume Analysis", "#f9a825", "🤖")
            html += _coming_soon("AI-powered strengths, weaknesses, skills and recommendations")

        except RuntimeError as e:
            html += _error_line(f"✗ &nbsp; Could not read PDF: {e}")
            logging.error(f"PDF read error for {fp}: {e}")
        except Exception as e:
            html += _error_line(f"✗ &nbsp; Unexpected error: {e}")
            logging.error(f"Worker exception for {fp}: {e}")

        self.result.emit(html)
        self.status.emit("● Ready · Analysis complete.")
        self.finished.emit()


# ══════════════════════════════════════════════════════════════════════════════
# Main Window — UI built entirely in Python
# ══════════════════════════════════════════════════════════════════════════════

def _divider() -> QFrame:
    line = QFrame()
    line.setObjectName("divider")
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    return line


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocumentScannerAI")
        self.setMinimumSize(900, 600)
        self.resize(1100, 720)
        self.selected_file: str | None = None
        self._last_scan: dict = {}
        self._thread: QThread | None = None
        self._worker: AnalysisWorker | None = None

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())
        root.addWidget(self._build_main())

        self.statusBar().setObjectName("statusBar")
        self.statusBar().showMessage("● Ready · No file selected")

    # ── Sidebar ────────────────────────────────────────────────────────────────

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(260)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo area
        logo_widget = QWidget()
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
        file_layout = QVBoxLayout(file_widget)
        file_layout.setContentsMargins(20, 20, 20, 12)
        file_layout.setSpacing(10)

        doc_label = QLabel("DOCUMENT")
        doc_label.setObjectName("sectionLabel")

        self.selectButton = QPushButton("  Select PDF")
        self.selectButton.setObjectName("selectButton")
        self.selectButton.setMinimumHeight(40)
        self.selectButton.setCursor(Qt.CursorShape.PointingHandCursor)
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
        analyze_layout = QVBoxLayout(analyze_widget)
        analyze_layout.setContentsMargins(20, 16, 20, 16)
        analyze_layout.setSpacing(10)

        analyze_label = QLabel("ANALYSIS")
        analyze_label.setObjectName("analyzeLabel")

        self.analyzeButton = QPushButton("  Run Analysis")
        self.analyzeButton.setObjectName("analyzeButton")
        self.analyzeButton.setMinimumHeight(40)
        self.analyzeButton.setEnabled(False)
        self.analyzeButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.analyzeButton.clicked.connect(self.start_analysis)

        analyze_layout.addWidget(analyze_label)
        analyze_layout.addWidget(self.analyzeButton)
        layout.addWidget(analyze_widget)

        # Spacer
        layout.addStretch()
        layout.addWidget(_divider())

        # Footer
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(20, 12, 20, 16)
        version = QLabel("v1.0.0  ·  MIT License")
        version.setObjectName("versionLabel")
        footer_layout.addWidget(version)
        layout.addWidget(footer)

        return sidebar

    # ── Main content ───────────────────────────────────────────────────────────

    def _build_main(self) -> QWidget:
        main = QWidget()
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

        layout.addWidget(top_bar)
        layout.addWidget(self.resultsTextEdit)

        return main

    # ── File selection ─────────────────────────────────────────────────────────

    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a PDF Document", "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if not file_path:
            return

        if not is_pdf_file(file_path):
            QMessageBox.critical(
                self, "Invalid File",
                f"Not a valid PDF:\n\n{os.path.basename(file_path)}\n\n"
                "Please select a genuine PDF document."
            )
            logging.warning(f"Invalid PDF rejected: {file_path}")
            return

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
                return

        self.selected_file = file_path
        self._last_scan = suspicious   # store so worker reuses it — no double scan
        self.fileLabel.setText(os.path.basename(file_path))
        self.analyzeButton.setEnabled(True)
        self.resultsTextEdit.clear()
        self.statusDot.setText("● Ready")
        self.statusBar().showMessage(f"Loaded: {os.path.basename(file_path)}")
        logging.info(f"File selected: {file_path}")

    # ── Analysis ───────────────────────────────────────────────────────────────

    def start_analysis(self):
        if not self.selected_file:
            return

        # If a previous thread is still alive, stop it cleanly before starting a new one
        if self._thread is not None and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait()
        self._thread = None
        self._worker = None

        self.analyzeButton.setEnabled(False)
        self.selectButton.setEnabled(False)
        self.resultsTextEdit.clear()
        self.statusDot.setText("● Running")
        self.statusBar().showMessage("Analyzing…")

        self._thread = QThread()
        self._worker = AnalysisWorker(self.selected_file, self._last_scan)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.result.connect(self.resultsTextEdit.setHtml)
        self._worker.status.connect(self.statusBar().showMessage)
        self._worker.status.connect(self._update_dot)
        self._worker.finished.connect(self._on_finished)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._reset_thread_refs)

        self._thread.start()

    def _update_dot(self, status: str):
        if "Scanning" in status:
            self.statusDot.setText("● Scanning")
        elif "Extracting" in status:
            self.statusDot.setText("● Extracting")
        elif "Ready" in status:
            self.statusDot.setText("● Ready")

    def _on_finished(self):
        self.analyzeButton.setEnabled(True)
        self.selectButton.setEnabled(True)

    def _reset_thread_refs(self):
        self._thread = None
        self._worker = None


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLE)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
