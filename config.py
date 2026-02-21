"""
config.py — Project Configuration and Constants

Centralized configuration for DocumentScannerAI.
"""

# Allowed file extensions for PDF selection
ALLOWED_EXTENSIONS = {'.pdf'}

# Ollama API settings
OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
OLLAMA_MODEL = "llama3.1:8b"

# AI Analysis parameters
AI_TEMPERATURE = 0.3    # Lower = more deterministic, focused responses (0.0-1.0)
AI_TOP_P = 0.9          # Nucleus sampling threshold for diversity
RESUME_MAX_WORDS = 3000 # Maximum words to send to AI (context limit protection)
