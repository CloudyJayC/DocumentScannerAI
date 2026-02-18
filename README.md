# DocumentScannerAI

A modular, AI-powered PDF document scanner and analyzer.

## Features
- PDF-only validation and secure text extraction
- Keyword frequency analysis
- AI-powered named entity recognition (spaCy)
- Modular structure for easy expansion (security, reporting, GUI)

## Setup
1. Install Python 3.12
2. Clone this repo and navigate to the project folder
3. Create a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

## Usage
Run the main program:
```
python main.py
```

## Project Structure
- `main.py` — Entry point
- `file_handlers/` — PDF text extraction
- `analysis/` — Keyword and AI analysis
- `security/` — Validation and error handling
- `reports/` — (Planned) Report generation
- `tests/` — Unit tests

## License
MIT
