# DocumentScannerAI

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![Ollama](https://img.shields.io/badge/AI-Ollama-000000)](https://ollama.com)

A PDF resume analyzer with a dark-themed GUI. Uses a local **Ollama LLM** (llama3.1:8b) to analyze resumes. All processing runs on your machine — nothing is sent to external servers.

---

## Features

- **Dark-themed GUI** — PyQt6 interface with sidebar controls, no terminal required
- **Progress Bar** — Visual indicator while analysis is running
- **PDF Validation** — Checks file extension and PDF magic number (`%PDF-`)
- **File Size Limit** — Enforces 50MB maximum to prevent memory issues
- **Security Scanning** — Scans for embedded JavaScript, auto-run actions, launch commands, and hidden files
- **Text Extraction** — Resume-specific cleanup via `pdfplumber`: detects section headers, fixes hyphenated breaks, removes junk lines, normalizes whitespace
- **Local AI Analysis** — Uses `llama3.1:8b` running locally:
  - Overall impression
  - Strengths
  - Weaknesses
  - Key skills
  - Recommendations
- **Privacy** — All processing stays on your machine. No API keys, no accounts, no telemetry
- **Logging** — Full audit trail written to `scanner.log`

---

## Requirements

- Python 3.10 or higher
- [Ollama](https://ollama.com) — local LLM platform (system install, not pip)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/CloudyJayC/DocumentScannerAI.git
cd DocumentScannerAI
```

### 2. Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama and pull the model

Download Ollama from https://ollama.com and install it like any normal program.

Then in a terminal:

```bash
ollama pull llama3.1:8b
```

This downloads ~4.7GB one time. The model stays cached on your machine.

### 5. Run the app

Open two terminals:

```bash
# Terminal 1 — keep this running
ollama serve

# Terminal 2
python gui_main.py
```

---

## Usage

1. Click **Select PDF** to open a file picker
2. The file is validated and scanned for malicious content immediately on selection
3. If suspicious elements are found you'll be prompted to confirm before continuing
4. Click **Run Analysis** to:
   - Run the security scan
   - Extract and clean the resume text silently
   - Send it to the local AI for analysis
5. Results appear in the main panel with colour-coded sections

AI analysis typically takes 10-60 seconds on first run while the model loads into memory. Subsequent runs on the same session are faster.

---

## Project Structure

```
DocumentScannerAI/
├── analysis/
│   └── ai_analysis.py          — Ollama LLM interface and JSON parsing
├── file_handlers/
│   └── pdf_handler.py          — PDF text extraction and cleaning
├── ui/
│   ├── main_window.py          — Main application window and UI logic
│   ├── workers.py              — Background worker threads
│   └── styles.py               — Application stylesheet
├── utils/
│   ├── logger.py               — Centralized logging configuration
│   ├── validators.py           — PDF validation and security scanning
│   └── html_helpers.py         — HTML rendering for results display
├── tests/
│   └── test_*.py               — Unit and integration tests
├── sample_resumes/             — Sample PDFs for testing
├── config.py                   — Centralized configuration
├── gui_main.py                 — Application entry point ← run this
├── requirements.txt
└── README.md
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `PyQt6` | GUI framework |
| `pdfplumber` | PDF text extraction |
| `requests` | HTTP utilities (tests and tooling) |
| `fpdf2` | PDF report export |
| Ollama (system) | Local LLM server |

---

## Running Tests

```bash
python -m pytest tests/
```

---

## Troubleshooting

**Ollama not connecting**
Make sure `ollama serve` is running in a separate terminal before launching the app.

**AI analysis times out**
First run is slowest — the model loads from disk into memory. Wait up to 5 minutes on first run. Subsequent runs are much faster. On Windows with an AMD GPU, Ollama runs on CPU (ROCm is Linux-only for AMD), which is slower but works fine.

**No text extracted**
The PDF may be image-only or encrypted. pdfplumber cannot extract text from scanned images.

**App won't launch**
Run `pip install -r requirements.txt` to make sure all dependencies are installed.

---

## Roadmap

- [x] PDF validation and malicious content detection
- [x] Resume-specific text extraction and cleaning
- [x] Professional dark-theme GUI
- [x] Local AI resume analysis (strengths, weaknesses, skills, recommendations)
- [x] Progress bar during AI analysis
- [x] Export analysis to PDF report
- [ ] Support for DOCX and TXT input
- [ ] Camera scanner integration (OpenCV)

---

## Author

Jason Cameron — [@CloudyJayC](https://github.com/CloudyJayC)

---

## License

MIT — see [LICENSE](LICENSE) for details.

## Acknowledgements

- [Ollama](https://ollama.com) — local LLM platform
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) — GUI framework
- [pdfplumber](https://github.com/jamesturk/pdfplumber) — PDF text extraction
- [Meta Llama 3.1](https://www.meta.com/research/llama/) — AI model
