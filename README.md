# DocumentScannerAI

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![Ollama](https://img.shields.io/badge/AI-Ollama-000000)](https://ollama.com)

A modular, AI-powered PDF resume scanner and analyzer with a professional dark-theme GUI built on **PyQt6**, powered by a local **Ollama LLM** (llama3.1:8b). All processing runs locally — no data is sent to external servers.

---

## Features

- **Professional GUI** — Dark-themed PyQt6 sidebar interface, no terminal required
- **Visual Progress Indicator** — Sleek indeterminate progress bar shows analysis status in real-time
- **PDF Validation** — Extension check + magic number (`%PDF-`) verification
- **Security Scanning** — Detects embedded JavaScript, auto-run actions, launch commands, and embedded files before analysis begins
- **Intelligent Text Extraction** — Resume-specific cleaning via `pdfplumber`: section header detection, hyphenated line break fixes, junk line removal, whitespace collapsing
- **Local AI Resume Analysis** — Structured analysis powered by `llama3.1:8b` running on your machine:
  - Overall impression
  - Strengths
  - Areas to improve
  - Key skills detected
  - Actionable recommendations
- **Privacy First** — Nothing leaves your machine. No API keys, no accounts, no telemetry
- **Full Logging** — Audit trail written to `scanner.log`

---

## Requirements

- Python 3.12
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
├── reports/
│   └── report_generator.py     — legacy report generator (unused by GUI)
├── security/
│   └── error_handling.py       — logging helpers (used by terminal mode)
├── tests/
│   └── test_all.py             — unit tests
├── sample_resumes/             — sample PDFs for testing
├── config.py                   — shared configuration
├── gui_main.py                 — GUI entry point ← run this
├── main.py                     — legacy terminal entry point
├── requirements.txt
└── README.md
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `PyQt6` | GUI framework |
| `pdfplumber` | PDF text extraction |
| `colorama` | Coloured output for terminal mode |
| `anthropic` | Reserved for future cloud AI option |
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
- [ ] Export analysis to PDF report
- [ ] Support for DOCX and TXT input
- [ ] Custom model selection in GUI
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
