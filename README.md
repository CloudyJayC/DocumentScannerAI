# DocumentScannerAI

A modular, AI-powered PDF document scanner and resume analyzer with a graphical user interface built on PyQt6.

## Features

- GUI interface — select and analyze PDFs without touching the terminal
- Two-layer PDF validation — extension check + magic number (`%PDF-`) verification
- Malicious content detection — scans for embedded JavaScript, auto-run actions, launch commands, and embedded files before analysis begins
- Clean text extraction via `pdfplumber` with resume-specific formatting (section headers detected, hyphenated line breaks rejoined, junk lines removed)
- AI-powered resume analysis — strengths, weaknesses, skills, and recommendations *(coming in next patch)*
- Full logging to `scanner.log`
- Terminal mode still available via `main.py`

## Project Structure

```
DocumentScannerAI/
├── analysis/               — AI analysis modules (next patch)
├── file_handlers/
│   └── pdf_handler.py      — PDF text extraction and cleaning
├── reports/
│   └── report_generator.py — text report generation
├── security/
│   └── error_handling.py   — logging and error helpers (terminal mode)
├── tests/
│   └── test_all.py         — unit tests
├── sample_resumes/         — sample PDFs for testing
├── config.py               — shared configuration
├── gui_main.py             — GUI entry point (PyQt6) ← run this
├── main.py                 — terminal entry point (CLI)
├── requirements.txt
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

   # macOS / Linux
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI (recommended)
```bash
python gui_main.py
```
Click **Select PDF** to open a file picker — the file is validated and scanned for malicious content immediately on selection. Click **Run Analysis** to extract and display the cleaned text.

### Terminal
```bash
python main.py
```
You will be prompted to enter the path to a PDF file.

## Running Tests
```bash
python -m pytest tests/
```

## Dependencies

| Package | Purpose |
|---|---|
| `PyQt6` | GUI framework |
| `pdfplumber` | PDF text extraction |
| `colorama` | Colored terminal output (terminal mode) |
| `anthropic` | AI resume analysis (next patch) |

## Roadmap

- [x] PDF validation and malicious content detection
- [x] Clean text extraction with resume formatting
- [x] Professional dark-theme GUI
- [ ] AI-powered resume strengths, weaknesses, and skills analysis
- [ ] Export analysis to PDF report

## License

MIT
