# DocumentScannerAI

A modular, AI-powered PDF scanner and resume analyzer with a professional graphical user interface built on PyQt6 and powered by a local Ollama LLM.

## Features

- **GUI Interface** — Select and analyze PDFs with a dark-themed PyQt6 interface (no terminal required)
- **Two-Layer PDF Validation** — Extension check + magic number (`%PDF-`) verification to ensure genuine PDF files
- **Malicious Content Detection** — Scans for embedded JavaScript, auto-run actions, launch commands, and embedded files before analysis begins
- **Clean Text Extraction** — Uses `pdfplumber` with resume-optimized formatting:
  - Detects and adds spacing before section headers
  - Fixes hyphenated line breaks (rejoins split words)
  - Removes junk lines, symbols, and page numbers
  - Collapses excessive whitespace
- **Local AI Analysis** — Uses llama3.1:8b running on your machine (via Ollama) for private, fast resume analysis
  - Structured analysis: overall impression, strengths, weaknesses, key skills, recommendations
  - No data sent to external servers
  - Graceful fallback if AI returns invalid JSON
  - Automatic brace escaping to handle special characters in resumes
- **Full Logging** — All operations logged to `scanner.log` for debugging and audit trails (auto-ignored by git)
- **Professional Dark Theme** — Accessible, modern UI with custom PyQt6 stylesheets

## Project Structure

```
DocumentScannerAI/
├── analysis/
│   ├── __init__.py
│   └── ai_analysis.py         — Ollama LLM interface for resume analysis
├── file_handlers/
│   ├── __init__.py
│   └── pdf_handler.py         — PDF extraction and text cleaning
├── tests/
│   ├── __init__.py
│   ├── test_all.py            — Unit tests for PDF handler and validation
│   └── test_pdf_handler_manual.py
├── sample_resumes/            — Sample PDFs for testing
├── config.py                  — Centralized configuration and constants
├── gui_main.py                — Main GUI entry point (PyQt6) ← RUN THIS
├── requirements.txt           — Python dependencies
├── LICENSE
└── README.md
```

## Requirements

- **Python 3.8+**
- **Ollama** — Local LLM platform (https://ollama.com)
  - Download and install from https://ollama.com
  - The llama3.1:8b model must be pulled (see Setup below)

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Installed packages:**
- `PyQt6` — GUI framework
- `pdfplumber` — PDF text extraction

### 2. Install and Configure Ollama

1. **Download Ollama** — Visit https://ollama.com and download for your OS (Windows, macOS, Linux)

2. **Install and Run**
   ```bash
   # Start Ollama (keep it running while using DocumentScannerAI)
   ollama serve
   ```

3. **Pull the llama3.1:8b Model** (first time only)
   ```bash
   ollama pull llama3.1:8b
   ```

   This downloads ~4.7GB. Subsequent runs will use the cached model.

### 3. Verify Setup

- Ollama should be running at `http://localhost:11434`
- The model `llama3.1:8b` should be available

## Usage

### Launch the GUI

```bash
python gui_main.py
```
Or on Windows:
```bash
py gui_main.py
```

**Workflow:**

1. Click **Select PDF** to open a file picker
2. The file is validated and scanned for malicious content immediately
3. If suspicious elements are found, you'll be prompted to confirm
4. Click **Run Analysis** to:
   - Display security scan results
   - Extract and display cleaned text
   - Run AI analysis for strengths, weaknesses, skills, and recommendations (may take 10-60 seconds)
5. Results appear in the main panel with color-coded sections

**Note:** AI analysis can take 10-60 seconds depending on resume length and your system. The app has a 5-minute timeout for complex analysis.ecommendations
5. Results appear in the main panel with color-coded sections

### Running Tests

```bash
python -m pytest tests/
```

Or run a specific test:

```bash
python -m pytest tests/test_all.py::TestPDFHandler::test_extract_returns_string -v
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `PyQt6` | Latest | GUI framework for the desktop application |
| `pdfplumber` | Latest | Reliable PDF text extraction with custom tolerances |

**System Requirements:**
- Ollama running locally with `llama3.1:8b` model pulled

## Configuration

Key settings can be customized in `config.py`:

```python
OLLAMA_HOST = "localhost"           # Ollama API host
OLLAMA_PORT = 11434                 # Ollama API port
OLLAMA_MODEL = "llama3.1:8b"        # Model name
AI_TEMPERATURE = 0.3                # Low = deterministic, High = creative (0.0-1.0)
RESUME_MAX_WORDS = 3000             # Max words sent to AI (context limit)
```

## Troubleshooting

If Ollama is running but still not connecting, verify:
- Ollama is listening on `http://localhost:11434`
- The `llama3.1:8b` model is pulled: `ollama pull llama3.1:8b`

### "No text could be extracted"

The PDF may be image-only or encrypted. Try another PDF file.

### AI Analysis Hangs or Takes Too Long

- Normal analysis takes 10-60 seconds
- The app has a 5-minute (300 second) timeout
- Check that your system has enough RAM (model uses ~4GB)
- Try restarting Ollama: `ollama serve`

### ecent Improvements

### v1.1 (Latest)
- ✅ **Fixed format string bug** — Automatic brace escaping prevents crashes with special characters
- ✅ **Graceful AI fallback** — App no longer crashes if AI returns invalid JSON
- ✅ **Project cleanup** — Removed empty modules, cache files, and temporary logs
- ✅ **Enhanced error handling** — More informative error messages and logging
- ✅ **Updated documentation** — Comprehensive README with troubleshooting

### v1.0
- ✅ PDF validation and malicious content detection
- ✅ Text extraction with resume-specific formatting
- ✅ Professional dark-theme GUI
- ✅ AI-powered analysis (strengths, weaknesses, skills, recommendations)

## Roadmap

- [ ] Export analysis to formatted PDF report
- [ ] Support for other document types (DOCX, TXT)
- [ ] Batch analysis for multiple files
- [ ] Progress indicator during AI analysis
- [ ] Custom AI model selection in GUI
**Fixed in current version!** The app now automatically escapes `{` and `}` characters in resume text to prevent format string conflicts
```bash
ollama serve
```

### "No text could be extracted"

The PDF may be image-only or encrypted. Try another PDF file.

### Tests Fail

Ensure the sample resume (`sample_resumes/sample.pdf`) exists or tests are skipped.

## Roadmap

- [x] PDF validation and malicious content detection
- [x] Text extraction with resume-specific formatting
- [x] Professional dark-theme GUI
- [x] AI-powered analysis (strengths, weaknesses, skills, recommendations)
- [ ] Export analysis to PDF report
- [ ] Support for other document types (DOCX, TXT)
- [ ] Batch analysis for multiple files

## License

MIT — See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
