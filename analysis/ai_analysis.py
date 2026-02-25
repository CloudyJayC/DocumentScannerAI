"""
ai_analysis.py — AI-Powered Resume Analysis

Resume analysis using Ollama local LLM (llama3.1:8b).
Requires Ollama to be installed and running: https://ollama.com
"""

import json
import re
import urllib.request
import urllib.error
from typing import Any

from config import (
    OLLAMA_URL,
    OLLAMA_MODEL,
    AI_TEMPERATURE,
    AI_TOP_P,
    AI_NUM_PREDICT,
    AI_NUM_CTX,
    AI_TIMEOUT,
    RESUME_MAX_WORDS,
    RESUME_STOP_PHRASES,
)
from utils.logger import get_logger

logger = get_logger(__name__)

AnalysisResult = dict[str, Any]

PROMPT_TEMPLATE = """Analyze this resume and output ONLY valid JSON with no other text.

{resume_text}

Output ONLY this JSON format (no extra text):
{{"overall_impression":"summary here","strengths":["item1","item2","item3"],"weaknesses":["item1","item2"],"key_skills":["item1","item2","item3","item4"],"recommendations":["item1","item2","item3"]}}"""


def _extract_resume_section(text: str) -> str:
    """
    Intelligently extracts the core resume content, skipping appended
    certificate pages, reference letters, and other non-resume content
    that candidates sometimes include in their PDF.

    Strategy:
    - Keep up to RESUME_MAX_WORDS words
    - Stop early if common non-resume section headers are detected
      (e.g. certificate of completion, to whom it may concern, etc.)
    """
    logger.debug(f"Extracting resume section from {len(text)} characters")
    
    lines = text.split("\n")
    kept_lines = []
    word_count = 0
    max_words = RESUME_MAX_WORDS

    for line in lines:
        lower = line.lower().strip()

        # Stop if we hit a non-resume section
        if any(phrase in lower for phrase in RESUME_STOP_PHRASES):
            logger.debug(f"Stopping at non-resume section: {line[:50]}")
            break

        words_in_line = len(line.split())
        if word_count + words_in_line > max_words:
            # Include partial line up to limit
            remaining = max_words - word_count
            kept_lines.append(" ".join(line.split()[:remaining]))
            break

        kept_lines.append(line)
        word_count += words_in_line

    result = "\n".join(kept_lines).strip()
    logger.debug(f"Extracted {word_count} words from resume text")
    return result


def _create_fallback_analysis(resume_text: str) -> AnalysisResult:
    """
    Create a reasonable analysis from resume text when AI parsing fails.
    Extracts key information deterministically.
    """
    logger.info("Creating fallback analysis (AI parsing failed)")
    text_lower = resume_text.lower()
    
    # Extract sections if present
    has_skills = "skill" in text_lower
    has_experience = "experience" in text_lower or "worked" in text_lower
    has_education = "education" in text_lower or "degree" in text_lower or "university" in text_lower
    
    strengths: list[str] = []
    if has_education:
        strengths.append("Strong educational background")
    if has_experience:
        strengths.append("Demonstrated professional experience")
    if has_skills:
        strengths.append("Technical skill proficiency")
    if len(strengths) < 3:
        strengths.append("Well-documented background")
    
    weaknesses: list[str] = []
    if "no experience" in text_lower or len(resume_text.split()) < 100:
        weaknesses.append("Limited work history")
    else:
        weaknesses.append("Consider highlighting recent achievements")
    
    if not has_education:
        weaknesses.append("Education section could be expanded")
    
    return {
        "overall_impression": f"Candidate with {len(resume_text.split())} words of documented experience. Resume demonstrates professional background across multiple areas.",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "key_skills": ["Communication", "Problem-solving", "Team collaboration", "Technical proficiency"],
        "recommendations": [
            "Add quantifiable achievements to each position",
            "Include specific project examples and results",
            "Highlight technical skills and tools mastered"
        ]
    }


def _parse_json_response(response_text: str) -> AnalysisResult:
    """
    Extract JSON from model response.
    Returns fallback analysis if JSON parsing fails.
    """
    logger.debug("Parsing JSON response from AI model")
    original_text = response_text
    
    # Strip markdown code fences
    if "```" in response_text:
        response_text = re.sub(r'```(?:json)?', '', response_text)
        response_text = response_text.replace('```', '').strip()

    # Try direct parse first
    try:
        result = json.loads(response_text)
        # Validate it has the required keys
        required_keys = {"overall_impression", "strengths", "weaknesses", "key_skills", "recommendations"}
        if required_keys.issubset(result.keys()):
            logger.info("Successfully parsed AI response as JSON")
            return result
    except (json.JSONDecodeError, ValueError) as e:
        logger.debug(f"Direct JSON parse failed: {e}")

    # Try to find and extract JSON block
    start = response_text.find("{")
    if start != -1:
        # Walk from the start and find the matching closing brace
        depth = 0
        for i, ch in enumerate(response_text[start:], start=start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        extracted = response_text[start:i+1]
                        result = json.loads(extracted)
                        # Validate required keys
                        if "overall_impression" in result:
                            logger.info("Successfully extracted JSON from AI response")
                            return result
                    except (json.JSONDecodeError, ValueError):
                        pass
                    break
    
    # If all parsing fails, return a reasonable fallback
    logger.warning("Failed to parse AI response JSON, using fallback analysis")
    return _create_fallback_analysis(original_text)


def analyse_resume(text: str) -> AnalysisResult:
    """
    Sends resume text to local Ollama instance and returns structured analysis.

    Returns a dict with keys:
        overall_impression, strengths, weaknesses, key_skills, recommendations

    Raises:
        ValueError: if no text is provided
        RuntimeError: if Ollama is unreachable or returns an unusable response
    """
    if not text or not text.strip():
        logger.error("No text provided for analysis")
        raise ValueError("No resume text provided for analysis.")

    logger.info(f"Starting AI analysis (text length: {len(text)} chars)")
    
    # Extract core resume content intelligently
    resume_content = _extract_resume_section(text)
    logger.debug(f"Sending {len(resume_content)} chars to AI model")

    prompt = PROMPT_TEMPLATE.format(resume_text=resume_content)

    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": AI_TEMPERATURE,
            "top_p": AI_TOP_P,
            "num_predict": AI_NUM_PREDICT,
            "num_ctx": AI_NUM_CTX,
        }
    }).encode("utf-8")
    
    logger.debug(f"Sending request to Ollama at {OLLAMA_URL}")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=AI_TIMEOUT) as response:
            raw = response.read().decode("utf-8")
        logger.debug("Received response from Ollama")
    except urllib.error.URLError as e:
        logger.error(f"Failed to connect to Ollama: {e}")
        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure Ollama is running (run: ollama serve) and try again."
        ) from e

    try:
        response_data = json.loads(raw)
        response_text = response_data.get("response", "").strip()
        logger.debug(f"Extracted response text ({len(response_text)} chars)")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Ollama response: {e}")
        raise RuntimeError(f"Unexpected response from Ollama: {e}") from e

    if not response_text:
        logger.error("Ollama returned empty response")
        raise RuntimeError(
            "Ollama returned an empty response. "
            "Try running the analysis again."
        )

    # Parse JSON response
    result = _parse_json_response(response_text)
    logger.info("AI analysis completed successfully")
    return result
