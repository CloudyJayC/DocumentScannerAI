# DocumentScannerAI

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modular, AI-powered PDF scanner and resume analyzer with a professional graphical user interface built on **PyQt6** and powered by a local **Ollama LLM** (llama3.1:8b).

## 🎯 Features

- **GUI Interface** — Dark-themed PyQt6 interface for seamless PDF analysis (no terminal required)
- **Robust PDF Validation** — Dual-layer verification (extension check + magic numbers) to ensure genuine PDF files
- **Security Scanning** — Detects malicious content before processing:
  - Embedded JavaScript detection
  - Auto-run action detection
  - Launch command detection
  - Embedded files detection
- **Intelligent Text Extraction** — Uses `pdfplumber` with resume-specific optimizations:
  - Intelligent spacing detection for section headers
  - Automatic hyphenated line break fixes
  - Junk line and symbol removal
  - Excessive whitespace collapsing
- **Local AI Analysis** — Uses `llama3.1:8b` running locally (via Ollama):
  - Structured resume analysis (impression, strengths, weaknesses, skills, recommendations)
  - Privacy-first: no data sent to external servers
  - Graceful fallback for invalid JSON responses
  - Automatic character escaping for special content
- **Comprehensive Logging** — Full audit trail in `scanner.log` (auto-excluded from git)
- **Accessible Design** — Modern dark theme with custom PyQt6 stylesheets

## 📋 Requirements

- **Python 3.8** or higher
- **Ollama** — Local LLM platform
  - Download from https://ollama.com
  - Requires `llama3.1:8b` model

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/DocumentScannerAI.git
cd DocumentScannerAI
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Ensure Ollama is Running

```bash
# In a separate terminal, start Ollama
ollama serve

# In another terminal, pull the model
ollama pull llama3.1:8b
```

### 5. Run the Application

```bash
python gui_main.py
```

## 📁 Project Structure

```
DocumentScannerAI/
├── .github/                      # GitHub templates and CI/CD
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
├── analysis/                     # AI analysis module
│   ├── __init__.py
│   └── ai_analysis.py           # Ollama LLM interface
├── file_handlers/                # PDF handling module
│   ├── __init__.py
│   └── pdf_handler.py           # PDF extraction & validation
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_all.py
│   ├── test_full_pipeline.py
│   ├── test_ollama_response.py
│   └── test_pdf_handler_manual.py
├── sample_resumes/               # Sample PDFs for testing
│   └── sample.pdf
├── config.py                     # Configuration & constants
├── gui_main.py                   # Main GUI entry point ← RUN THIS
├── setup.py                      # Package setup configuration
├── requirements.txt              # Python dependencies
├── LICENSE                       # MIT License
├── README.md                     # This file
└── CONTRIBUTING.md               # Contribution guidelines
```

## 🛠 Usage

### GUI Mode (Recommended)

```bash
python gui_main.py
```

1. Launch the application
2. Click "Select PDF" to choose a resume
3. The application automatically:
   - Validates the PDF integrity
   - Scans for malicious content
   - Extracts and cleans text
   - Analyzes with AI
4. View results in the analysis panel

### Command Line Mode (Testing)

```bash
python -m pytest tests/
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
OLLAMA_HOST = "localhost"           # Ollama server address
OLLAMA_PORT = 11434                 # Ollama server port
OLLAMA_MODEL = "llama3.1:8b"        # Model to use
AI_TEMPERATURE = 0.3                # Model creativity (0.0-1.0)
AI_TOP_P = 0.9                      # Nucleus sampling parameter
RESUME_MAX_WORDS = 3000             # Max words to send to AI
```

## 🔒 Security Features

### PDF Validation
- ✅ Extension verification (`.pdf` only)
- ✅ Magic number validation (`%PDF-` header)
- ✅ Malicious content scanning

### Data Privacy
- ✅ All processing runs locally
- ✅ No telemetry or data collection
- ✅ Can run completely offline (after model download)

## 📊 Analysis Output

The AI analyzer returns structured JSON:

```json
{
  "overall_impression": "Strong technical background with clear communication skills",
  "strengths": ["Experience with multiple languages", "Good project portfolio"],
  "weaknesses": ["Limited management experience"],
  "key_skills": ["Python", "JavaScript", "React"],
  "recommendations": ["Consider adding metrics to achievements", "Expand leadership examples"]
}
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_full_pipeline.py

# Run with verbose output
python -m pytest tests/ -v
```

Test files included:
- `test_all.py` — Unit tests for PDF handler and validation
- `test_full_pipeline.py` — End-to-end pipeline testing
- `test_ollama_response.py` — Ollama API response testing
- `test_pdf_handler_manual.py` — Manual PDF handler testing

## 🐛 Troubleshooting

### Ollama Connection Error
```
Error: Connection refused [localhost:11434]
```
**Solution:** Ensure Ollama is running (`ollama serve`) and the model is installed (`ollama pull llama3.1:8b`)

### Invalid JSON Response from AI
```
Warning: Failed to parse AI response JSON
```
**Solution:** The app has graceful fallback. Check `scanner.log` for details. Try adjusting `AI_TEMPERATURE` in `config.py`

### GUI Not Launching
```
ModuleNotFoundError: No module named 'PyQt6'
```
**Solution:** Install dependencies: `pip install -r requirements.txt`

### PDF Not Found
- Verify PDF exists at the selected path
- Check file permissions
- Ensure PDF is not corrupted

## 📝 Logging

All operations are logged to `scanner.log`:

```bash
# View recent logs
tail -f scanner.log

# Search for errors
grep ERROR scanner.log
```

Log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Write tests for new functionality
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## 👨‍💻 Author

Your Name — [@yourhandle](https://github.com/yourusername)

## 🙏 Acknowledgments

- [Ollama](https://ollama.com) — Local LLM platform
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) — GUI framework
- [pdfplumber](https://github.com/jamesturk/pdfplumber) — PDF text extraction
- [llama3.1](https://www.meta.com/research/llama/) — AI model

## 📞 Support

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yourusername/DocumentScannerAI/issues)
- 💬 [Discussions](https://github.com/yourusername/DocumentScannerAI/discussions)

---

**⭐ If you find this useful, please consider giving it a star!**

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
