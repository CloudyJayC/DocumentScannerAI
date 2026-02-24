"""
styles.py — Application Stylesheet

Dark-themed PyQt6 stylesheet for DocumentScannerAI.
Defines colors, fonts, and styling for all UI components.
"""

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
    color: #4a5568;
    font-size: 10px;
}
QLabel#sectionLabel, QLabel#analyzeLabel {
    color: #4a5568;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
}
QLabel#fileLabelHeader {
    color: #4a6080;
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
    color: #64748b;
    font-size: 11px;
}


QWidget#logoArea, QWidget#fileSection, QWidget#analyzeSection,
QWidget#sidebarFooter, QWidget#mainContent {
    border: none;
}
QWidget#fileInfoBox {
    background-color: #0d1120;
    border: 1px solid #243044;
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

QPushButton#exportButton {
    background-color: #1a2a3a;
    color: #7dd3fc;
    border: 1px solid #2a4a6a;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 600;
    text-align: left;
}
QPushButton#exportButton:hover {
    background-color: #1e3a50;
    border-color: #3b82f6;
    color: #bfdbfe;
}
QPushButton#exportButton:pressed {
    background-color: #162840;
}
QPushButton#exportButton:disabled {
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
QTextEdit#resultsTextEdit[placeholderText] {
    color: #374151;
}

QProgressBar#analysisProgress {
    background-color: #0a0d14;
    border: none;
    max-height: 6px;
    min-height: 6px;
    text-align: center;
}
QProgressBar#analysisProgress::chunk {
    background-color: #6ee7b7;
    border: none;
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
    color: #64748b;
    font-size: 10px;
    border-top: 1px solid #1e2433;
    padding: 0 12px;
}


QToolTip {
    background-color: #1a2035;
    color: #cbd5e1;
    border: 1px solid #2a3654;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
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
