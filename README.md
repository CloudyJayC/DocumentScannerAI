# DocumentScannerAI

A modular, AI-powered PDF document scanner and analyzer with a graphical user interface built on PyQt6.

## Features

- GUI interface — select and analyze PDFs without touching the terminal
- Two-layer PDF validation — extension check + magic number (`%PDF-`) verification
- Malicious content detection — scans for embedded JavaScript, auto-run actions, launch commands, and embedded files before analysis begins
- Text extraction via `pdfplumber`
- Keyword frequency analysis with stopword filtering
- AI-powered named entity recognition using spaCy (people, organizations, locations, dates, and more)
- Automatic text report generation saved alongside the analyzed file
- Full logging to `scanner.log`
- Terminal mode still available via `main.py`

## Project Structure

```
DOCUMENTSCANNERAI/
├── analysis/
│   ├── ai_analysis.py          — spaCy NLP entity extraction and summarization
│   └── keyword_analysis.py     — keyword frequency analysis
├── file_handlers/
│   └── pdf_handler.py          — PDF text extraction using pdfplumber
├── reports/
│   └── report_generator.py     — generates and saves text analysis reports
├── security/
│   ├── utils/                  — internal security utilities
│   ├── error_handling.py       — logging and error/warning helpers
│   └── validation.py           — PDF validation and pdfid stub scanner
├── tests/
│   ├── test_all.py
│   ├── test_keyword_analysis.py
│   ├── test_pdf_handler.py
│   └── test_pdf_handler_manual.py
├── sample_resumes/             — sample PDFs for testing
├── config.py                   — shared config (allowed extensions, etc.)
├── gui_main.py                 — GUI entry point (PyQt6) ← run this
├── main.py                     — terminal entry point (CLI)
├── Main.ui                     — Qt Designer UI layout file
├── requirements.txt
├── scanner.log                 — auto-generated runtime log
└── README.md
```

## Setup

1. **Install Python 3.12**

2. **Clone the repo and navigate into it**

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

## Usage

### GUI (recommended)
```bash
python gui_main.py
```
Click **Select PDF Document** to open a file picker, then click **Analyze Document**. Results stream into the output panel and a report is saved automatically.

### Terminal
```bash
python main.py
```
You will be prompted to enter the path to a PDF file. Results are printed to the console and a report is saved.

## Running Tests
```bash
python -m pytest tests/
```

## Dependencies

| Package | Purpose |
|---|---|
| `PyQt6` | GUI framework |
| `pdfplumber` | PDF text extraction |
| `spacy` + `en_core_web_sm` | Named entity recognition |
| `colorama` | Colored terminal output (terminal mode) |

## License

MIT
