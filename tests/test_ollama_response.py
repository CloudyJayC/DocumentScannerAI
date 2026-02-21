#!/usr/bin/env python3
"""Test what Ollama actually returns."""

import json
import urllib.request
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

prompt = """Return this JSON:
{"result": "test", "value": 123}

Just return the JSON, nothing else."""

payload = json.dumps({
    "model": MODEL,
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.1,
        "top_p": 0.9,
        "num_predict": 50,
        "num_ctx": 3072,
    }
}).encode("utf-8")

print("Sending request to Ollama...")
print(f"Prompt: {prompt}")
print()

try:
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=60) as response:
        raw = response.read().decode("utf-8")
        print("Raw response:")
        print(raw)
        print()
        
        data = json.loads(raw)
        response_text = data.get("response", "")
        print("Response text:")
        print(response_text)
        print()
        
        print("Attempting to parse as JSON...")
        try:
            result = json.loads(response_text)
            print("Successfully parsed:", result)
        except Exception as e:
            print(f"Failed to parse: {e}")
            
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
