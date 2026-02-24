"""
config.py — Project Configuration and Constants

Centralized configuration for DocumentScannerAI.
All configuration values used throughout the application.
"""

# ══════════════════════════════════════════════════════════════════════════════
# File Validation
# ══════════════════════════════════════════════════════════════════════════════

# Allowed file extensions for PDF selection
ALLOWED_EXTENSIONS = {'.pdf'}

# PDF magic number for validation
PDF_MAGIC_NUMBER = b"%PDF-"


# ══════════════════════════════════════════════════════════════════════════════
# Security Scanning
# ══════════════════════════════════════════════════════════════════════════════

# Suspicious PDF features to scan for
SUSPICIOUS_PDF_KEYWORDS = {
    "/JS": 0,              # JavaScript in PDF
    "/JavaScript": 0,      # JavaScript object
    "/AA": 0,              # Auto-Action (triggers on open)
    "/OpenAction": 0,      # Action on document open
    "/Launch": 0,          # Launch external program
    "/EmbeddedFile": 0,    # Embedded files (can hide malware)
    "/AcroForm": 0,        # Interactive forms
    "/RichMedia": 0,       # Embedded media (Flash, etc.)
}


# ══════════════════════════════════════════════════════════════════════════════
# Ollama AI Settings
# ══════════════════════════════════════════════════════════════════════════════

# Ollama server connection
OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"

# AI model configuration
OLLAMA_MODEL = "llama3.1:8b"

# AI analysis parameters
AI_TEMPERATURE = 0.1    # Lower = more deterministic (0.0-1.0)
AI_TOP_P = 0.9          # Nucleus sampling threshold for diversity
AI_NUM_PREDICT = 512    # Max tokens to generate
AI_NUM_CTX = 3072       # Context window size
AI_TIMEOUT = 300        # Request timeout in seconds


# ══════════════════════════════════════════════════════════════════════════════
# Text Extraction & Processing
# ══════════════════════════════════════════════════════════════════════════════

# PDF text extraction tolerances
PDF_X_TOLERANCE = 2     # Horizontal spacing tolerance
PDF_Y_TOLERANCE = 3     # Vertical spacing tolerance

# Resume text processing
RESUME_MAX_WORDS = 1200  # Maximum words to send to AI (context limit)

# Section header detection keywords
RESUME_SECTION_HEADERS = {
    # Education
    "education", "academic", "qualifications", "degree", "credentials",
    # Experience/Work
    "experience", "employment", "work experience", "career history", 
    "professional experience", "positions held", "work history", "job history",
    "professional background",
    # Skills
    "skills", "technical skills", "core competencies", "competencies", "expertise",
    "proficiencies", "abilities", "capabilities", "areas of expertise",
    # Summary
    "summary", "professional summary", "executive summary", "profile", "objective",
    "career objective", "professional objective", "about", "about me",
    # Certifications/Training
    "certifications", "certification", "certified", "licenses", "license", "training",
    "professional development", "courses", "accreditations",
    # Projects
    "projects", "portfolio", "key projects", "notable projects",
    # Additional
    "awards", "honors", "recognition", "achievements", "accomplishments",
    "languages", "language", "volunteer", "volunteering", "volunteer work",
    "publications", "references", "contact", "contact information", "details",
    "interests", "additional", "activities", "involvement", "leadership",
    "technical expertise", "knowledge", "tools", "technologies", 
    "technical proficiencies",
}

# Resume content filtering (stop phrases for non-resume content)
RESUME_STOP_PHRASES = [
    "certificate of", "this is to certify", "to whom it may concern",
    "reference letter", "dear hiring", "dear sir", "dear madam",
    "letter of recommendation", "hereby certify", "certificate number",
    "completion certificate", "awarded to", "this certifies",
]


# ══════════════════════════════════════════════════════════════════════════════
# Logging
# ══════════════════════════════════════════════════════════════════════════════

# Log file configuration
LOG_FILE = "scanner.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL


# ══════════════════════════════════════════════════════════════════════════════
# GUI Settings
# ══════════════════════════════════════════════════════════════════════════════

# Application metadata
APP_NAME = "DocumentScannerAI"
APP_VERSION = "1.1.0"
APP_LICENSE = "MIT License"

# Window dimensions
WINDOW_MIN_WIDTH = 960
WINDOW_MIN_HEIGHT = 640
WINDOW_DEFAULT_WIDTH = 1100
WINDOW_DEFAULT_HEIGHT = 720

# Sidebar dimensions
SIDEBAR_WIDTH = 260
