"""
gui_main.py — DocumentScannerAI GUI Entry Point (PyQt6)
========================================================
Loads Main.ui and connects all existing analysis logic to the GUI.

Place this file in your project root, alongside Main.ui:

  project/
  ├── gui_main.py         ← this file
  ├── Main.ui
  ├── main.py
  ├── file_handlers/
  │   └── pdf_handler.py
  ├── analysis/
  │   ├── keyword_analysis.py
  │   └── ai_analysis.py
  ├── security/
  │   └── ...
  └── reports/
      └── report_generator.py

Run with:
  python gui_main.py
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import QThread, pyqtSignal, QObject

# ── Your existing modules (matching your subfolder structure) ──────────────────
from file_handlers.pdf_handler import extract_text_from_pdf
from analysis.keyword_analysis import analyze_keywords
from analysis.ai_analysis import ai_analyze_text
from reports.report_generator import generate_text_report

# ── Logging setup (mirrors error_handling.py but GUI-friendly) ─────────────────
logging.basicConfig(
    filename="scanner.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)


# ══════════════════════════════════════════════════════════════════════════════
# Validation — inlined here so we don't depend on config.py / pdfid_stub.py
# ══════════════════════════════════════════════════════════════════════════════

ALLOWED_EXTENSIONS = {".pdf"}

def is_pdf_file(file_path: str) -> bool:
    """
    Two-layer PDF check:
      1. File extension must be .pdf
      2. File must start with the PDF magic number (%PDF-)
    """
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
    """
    Scans the raw PDF bytes for known dangerous keywords.
    Returns a dict of { element_name: count } for anything suspicious found.
    This is a lightweight heuristic scan — not a replacement for a full AV tool.

    Dangerous indicators checked:
      /JS / /JavaScript  — embedded JavaScript (common in exploits)
      /AA / /OpenAction  — auto-actions that run on open
      /Launch            — can execute external programs
      /EmbeddedFile      — hidden file attachments
      /AcroForm          — interactive forms (lower risk, flagged for info)
      /RichMedia         — Flash/media embeds (legacy attack vector)
    """
    suspicious_keywords = {
        "/JS": 0,
        "/JavaScript": 0,
        "/AA": 0,
        "/OpenAction": 0,
        "/Launch": 0,
        "/EmbeddedFile": 0,
        "/AcroForm": 0,
        "/RichMedia": 0,
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
# Worker — runs the heavy analysis in a background thread so the UI never freezes
# ══════════════════════════════════════════════════════════════════════════════

class AnalysisWorker(QObject):
    """
    Runs the full pipeline (scan → extract → keyword → AI → report) off the
    main thread. Emits signals back to the GUI so everything stays responsive.
    """
    progress = pyqtSignal(str)   # plain progress / info lines
    warning  = pyqtSignal(str)   # orange warnings
    error    = pyqtSignal(str)   # red errors
    finished = pyqtSignal()      # emitted when done (success or fail)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def run(self):
        fp = self.file_path
        self.progress.emit(f"Analyzing: {os.path.basename(fp)}\n")

        # ── Step 1: Security scan ──────────────────────────────────────────────
        self.progress.emit("🔍 Scanning for suspicious PDF elements...")
        suspicious = scan_pdf_for_malicious_content(fp)
        found = {k: v for k, v in suspicious.items() if v > 0}

        if found:
            self.warning.emit("⚠️  Suspicious elements detected:")
            for element, count in found.items():
                self.warning.emit(f"     {element}: {count} occurrence(s)")
            self.warning.emit(
                "\nProceed with caution. This file may contain active content.\n"
            )
            logging.warning(f"Suspicious elements in {fp}: {found}")
        else:
            self.progress.emit("✅ Security scan passed — no suspicious elements found.\n")
            logging.info(f"Clean file: {fp}")

        # ── Step 2: Text extraction ────────────────────────────────────────────
        self.progress.emit("📄 Extracting text from PDF...")
        text = extract_text_from_pdf(fp)

        if not text:
            self.error.emit("❌ No text could be extracted from this PDF.")
            self.error.emit("   The file may be scanned/image-only or encrypted.")
            logging.error(f"No text extracted: {fp}")
            self.finished.emit()
            return

        preview = text[:400].replace("\n", " ")
        self.progress.emit(f"Preview: {preview}…\n")

        # ── Step 3: Keyword analysis ───────────────────────────────────────────
        self.progress.emit("─── Keyword Analysis ────────────────────────────")
        kw = analyze_keywords(text)
        self.progress.emit(f"Total words  : {kw['word_count']}")
        self.progress.emit(f"Unique words : {kw['unique_words']}")
        self.progress.emit("Top 10 keywords:")
        for word, freq in kw["keywords"]:
            bar = "█" * min(freq, 30)
            self.progress.emit(f"   {word:<20} {freq:>4}  {bar}")
        self.progress.emit("")
        logging.info(f"Keyword analysis done: {fp}")

        # ── Step 4: AI / NLP entity analysis ──────────────────────────────────
        self.progress.emit("─── AI-Powered Entity Analysis ──────────────────")
        ai = ai_analyze_text(text)

        if "error" in ai:
            self.warning.emit(f"⚠️  AI Analysis unavailable: {ai['error']}")
            logging.warning(f"AI error for {fp}: {ai['error']}")
        else:
            self.progress.emit("Summary (first 3 sentences):")
            self.progress.emit(ai["summary"])
            self.progress.emit("")

            label_names = {
                "PERSON":  "👤 People",
                "ORG":     "🏢 Organizations",
                "GPE":     "📍 Locations",
                "DATE":    "📅 Dates",
                "PERCENT": "📊 Percentages",
                "CARDINAL":"🔢 Numbers",
                "LAW":     "⚖️  Legal References",
                "NORP":    "🌐 Groups / Nationalities",
            }
            grouped = ai.get("entities_grouped", {})
            if grouped:
                for label, ents in grouped.items():
                    unique_ents = sorted(set(ents))
                    if unique_ents:
                        header = label_names.get(label, f"📌 {label}")
                        self.progress.emit(f"{header}:")
                        for ent in unique_ents:
                            self.progress.emit(f"   • {ent}")
                        self.progress.emit("")
            else:
                self.progress.emit("No named entities found.")
            logging.info(f"AI analysis done: {fp}")

        # ── Step 5: Save report ────────────────────────────────────────────────
        try:
            report_path = generate_text_report(fp, suspicious, kw, ai)
            self.progress.emit(f"💾 Report saved to:\n   {report_path}\n")
            logging.info(f"Report saved: {report_path}")
        except Exception as e:
            self.warning.emit(f"⚠️  Could not save report: {e}")
            logging.error(f"Report error: {e}")

        self.finished.emit()


# ══════════════════════════════════════════════════════════════════════════════
# Main Window
# ══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the Qt Designer file — must be in the same directory as this script
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Main.ui")
        loadUi(ui_path, self)

        self.setWindowTitle("DocumentScannerAI")
        self.selected_file: str | None = None

        # Wire up buttons to methods
        self.selectButton.clicked.connect(self.select_pdf)
        self.analyzeButton.clicked.connect(self.start_analysis)

        # Thread references kept alive during analysis
        self._thread: QThread | None = None
        self._worker: AnalysisWorker | None = None

    # ── File selection ─────────────────────────────────────────────────────────

    def select_pdf(self):
        """Open file explorer filtered to PDF files, then validate the selection."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a PDF Document",
            "",                                         # start in last-used dir
            "PDF Files (*.pdf);;All Files (*)"
        )

        if not file_path:
            return  # user cancelled the dialog

        # ── Layer 1: extension + magic number check ────────────────────────────
        if not is_pdf_file(file_path):
            QMessageBox.critical(
                self,
                "Invalid File",
                f"The selected file is not a valid PDF:\n\n{os.path.basename(file_path)}\n\n"
                "Please choose a file that is a genuine PDF document."
            )
            logging.warning(f"Invalid PDF rejected: {file_path}")
            return

        # ── Layer 2: quick malicious content pre-check ─────────────────────────
        suspicious = scan_pdf_for_malicious_content(file_path)
        found = {k: v for k, v in suspicious.items() if v > 0}

        if found:
            details = "\n".join(f"  {k}: {v} occurrence(s)" for k, v in found.items())
            reply = QMessageBox.warning(
                self,
                "⚠️ Suspicious File Detected",
                f"This PDF contains potentially dangerous elements:\n\n{details}\n\n"
                "It may contain JavaScript, embedded files, or auto-run actions.\n\n"
                "Do you still want to proceed?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No       # default to No (safer choice)
            )
            if reply != QMessageBox.StandardButton.Yes:
                self.statusbar.showMessage("File rejected — suspicious content.")
                return

        # ── File accepted — update UI ──────────────────────────────────────────
        self.selected_file = file_path
        self.fileLabel.setText(os.path.basename(file_path))
        self.analyzeButton.setEnabled(True)
        self.resultsTextEdit.clear()
        self.statusbar.showMessage(f"Ready: {os.path.basename(file_path)}")
        logging.info(f"File selected: {file_path}")

    # ── Analysis ───────────────────────────────────────────────────────────────

    def start_analysis(self):
        """Kick off the full analysis pipeline in a background thread."""
        if not self.selected_file:
            return

        # Lock the UI while the worker runs
        self.analyzeButton.setEnabled(False)
        self.selectButton.setEnabled(False)
        self.resultsTextEdit.clear()
        self.statusbar.showMessage("Analyzing — please wait…")

        # Create worker and move it to a background thread
        self._thread = QThread()
        self._worker = AnalysisWorker(self.selected_file)
        self._worker.moveToThread(self._thread)

        # Connect worker signals to GUI slots
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self.append_normal)
        self._worker.warning.connect(self.append_warning)
        self._worker.error.connect(self.append_error)
        self._worker.finished.connect(self.on_analysis_finished)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    def on_analysis_finished(self):
        """Re-enable the UI after analysis completes."""
        self.analyzeButton.setEnabled(True)
        self.selectButton.setEnabled(True)
        self.statusbar.showMessage("Analysis complete.")

    # ── Output helpers ─────────────────────────────────────────────────────────

    def append_normal(self, text: str):
        """Append a plain text line to the results box."""
        self.resultsTextEdit.append(text)

    def append_warning(self, text: str):
        """Append an orange-coloured warning line."""
        self.resultsTextEdit.append(
            f'<span style="color:#e67e22;">{text}</span>'
        )

    def append_error(self, text: str):
        """Append a bold red error line."""
        self.resultsTextEdit.append(
            f'<span style="color:#e74c3c;font-weight:bold;">{text}</span>'
        )


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
