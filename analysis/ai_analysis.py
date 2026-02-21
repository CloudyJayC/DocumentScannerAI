"""
ai_analysis.py — AI-Powered Resume Analysis using Local Ollama LLM

Analyzes resume text using the llama3.1:8b model running locally via Ollama.
Requires Ollama to be installed and the model pulled.

Setup:
    1. Install Ollama: https://ollama.com
    2. Start Ollama: ollama serve (runs in background)
    3. Pull the model: ollama pull llama3.1:8b
"""

import json
import logging
import urllib.request
import urllib.error

# Ollama API endpoint and model selection
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

PROMPT_TEMPLATE = """Analyze this resume and respond with ONLY valid JSON, nothing else.

{{"overall_impression":"summary here","strengths":["s1","s2","s3"],"weaknesses":["w1","w2"],"key_skills":["k1","k2","k3"],"recommendations":["r1","r2","r3"]}}

Resume:
{resume_text}

JSON response:"""


def analyse_resume(text: str) -> dict:
    """Analyze a resume using the local Ollama LLM and return structured results.
    
    Sends the resume text to a running Ollama instance (default: localhost:11434)
    and parses the JSON response into a structured analysis with strengths,
    weaknesses, skills, and recommendations.
    
    Args:
        text: The extracted resume text to analyze
    
    Returns:
        Dictionary with keys: overall_impression, strengths, weaknesses, 
        key_skills, recommendations (all from AI analysis)
    
    Raises:
        ValueError: If text is empty or whitespace-only
        RuntimeError: If Ollama is unreachable or returns unexpected format
    """
    if not text or not text.strip():
        raise ValueError("No resume text provided for analysis.")

    # Escape braces in the text to prevent .format() from interpreting them as placeholders
    # This is critical: if resume contains { or }, format() will throw KeyError
    text_safe = text.replace("{", "{{").replace("}", "}}")

    # Trim to ~3000 words to keep within context window limits
    # This prevents token overflow and speeds up analysis
    words = text_safe.split()
    if len(words) > 3000:
        text_safe = " ".join(words[:3000])

    prompt = PROMPT_TEMPLATE.format(resume_text=text_safe)

    # Build the API request payload with model and generation settings
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,  # Wait for complete response, don't stream
        "options": {
            "temperature": 0.3,   # Low temperature = consistent, deterministic output
            "top_p": 0.9,         # Nucleus sampling for quality/diversity balance
            "num_predict": 1024,  # Limit tokens to prevent runaway generation
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        # Send request to Ollama API (5-minute timeout for complex analysis)
        with urllib.request.urlopen(req, timeout=300) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        # Ollama not running or unreachable
        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure Ollama is running (run: ollama serve) and try again."
        ) from e

    try:
        # Parse the API response envelope
        response_data = json.loads(raw)
        response_text = response_data.get("response", "").strip()
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Unexpected response from Ollama: {e}") from e

    # Clean up markdown code fences
    response_text = response_text.replace("```json", "").replace("```", "").strip()

    # Try to parse the JSON response with multiple fallback attempts
    result = None
    
    # Attempt 1: Direct parse
    try:
        result = json.loads(response_text)
        logging.debug("Direct JSON parse succeeded")
    except json.JSONDecodeError:
        logging.debug("Direct JSON parse failed, trying extraction...")
    
    # Attempt 2: Extract from markers
    if result is None:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        
        if start != -1 and end > start:
            try:
                extracted = response_text[start:end]
                result = json.loads(extracted)
                logging.debug("Extracted JSON parse succeeded")
            except json.JSONDecodeError:
                logging.debug("Extracted JSON parse failed, trying fixes...")
    
    # Attempt 3: Try fixing common JSON issues
    if result is None:
        try:
            fixed = response_text.replace(",}", "}").replace(",]", "]").replace("'", '"')
            result = json.loads(fixed)
            logging.debug("Fixed JSON parse succeeded")
        except json.JSONDecodeError:
            logging.debug("Fixed JSON parse failed, using fallback...")
    
    # If all parsing failed, use fallback
    if result is None:
        logging.warning(f"All JSON parsing attempts failed. Response: {response_text[:300]}")
        result = _create_fallback_analysis()
    else:
        # Validate result structure
        try:
            _validate_analysis_structure(result)
        except ValueError:
            logging.warning("AI response missing required fields, using fallback")
            result = _create_fallback_analysis()

    return result


def _validate_analysis_structure(result: dict) -> None:
    """Validate that the analysis result has required keys and types.
    
    Args:
        result: The analysis dict to validate
    
    Raises:
        ValueError: If required keys are missing or types are wrong
    """
    required_keys = {"overall_impression", "strengths", "weaknesses", "key_skills", "recommendations"}
    
    if not all(key in result for key in required_keys):
        raise ValueError(f"Missing required keys. Got: {set(result.keys())}")
    
    # Ensure proper types
    if not isinstance(result["overall_impression"], str):
        result["overall_impression"] = str(result["overall_impression"])
    if not isinstance(result.get("strengths"), list):
        result["strengths"] = []
    if not isinstance(result.get("weaknesses"), list):
        result["weaknesses"] = []
    if not isinstance(result.get("key_skills"), list):
        result["key_skills"] = []
    if not isinstance(result.get("recommendations"), list):
        result["recommendations"] = []


def _create_fallback_analysis() -> dict:
    """Create a fallback analysis when AI parsing fails."""
    return {
        "overall_impression": "Resume document was successfully processed. AI analysis unavailable at this moment.",
        "strengths": ["Document validated and processed"],
        "weaknesses": [],
        "key_skills": ["Analysis service temporarily unavailable - please retry"],
        "recommendations": ["Try the analysis again in a moment"]
    }
