#!/usr/bin/env python3
"""Test the complete resume analysis pipeline."""

from file_handlers.pdf_handler import extract_text_from_pdf
from analysis.ai_analysis import analyse_resume
import json
import os

def test_pipeline():
    pdf_path = 'sample_resumes/sample.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found")
        return
    
    print("Testing full pipeline...")
    print()
    
    print("Step 1: Extracting resume text")
    text = extract_text_from_pdf(pdf_path)
    print(f"✓ Extracted {len(text.split())} words")
    print()
    
    print("Step 2: Running AI analysis")
    result = analyse_resume(text)
    print("✓ Analysis complete!")
    print()
    
    print("Results:")
    print(json.dumps(result, indent=2))
    
    # Verify all required fields
    required = {"overall_impression", "strengths", "weaknesses", "key_skills", "recommendations"}
    missing = required - set(result.keys())
    
    if missing:
        print(f"\nⓘ Warning: Missing fields: {missing}")
    else:
        print("\n✓ All required fields present")

if __name__ == "__main__":
    test_pipeline()
