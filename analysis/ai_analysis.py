# AI-powered analysis using spaCy
# Extracts summary and named entities from text using spaCy NLP.
import spacy

# Load the small English model (download with: python -m spacy download en_core_web_sm)
try:
	nlp = spacy.load("en_core_web_sm")
except OSError:
	nlp = None

def ai_analyze_text(text):
	"""
	Analyze text using spaCy for summary and named entities.
	Returns a dict with:
	  - summary: first 3 sentences
	  - entities: list of (entity, label) tuples
	  - error: error message if spaCy model is not loaded
	"""
	if not nlp:
		return {"error": "spaCy model not loaded. Run: python -m spacy download en_core_web_sm"}
	doc = nlp(text)
	# Simple extractive summary: first 3 sentences
	summary = " ".join([sent.text for sent in list(doc.sents)[:3]])
	# Extract named entities, filter out single lowercase words and common false positives
	filtered_ents = []
	for ent in doc.ents:
		# Filter out single lowercase words and common false positives
		if len(ent.text.strip()) < 2:
			continue
		if ent.text.strip().islower() and len(ent.text.strip().split()) == 1:
			continue
		if ent.label_ == "PERSON" and ent.text.strip().lower() in {"junior", "diploma", "docker", "linux", "problem"}:
			continue
		filtered_ents.append((ent.text.strip(), ent.label_))
	# Group entities by label
	from collections import defaultdict
	grouped = defaultdict(list)
	for ent, label in filtered_ents:
		grouped[label].append(ent)
	return {
		"summary": summary,
		"entities": filtered_ents,
		"entities_grouped": dict(grouped)
	}
# AI/NLP-based analysis (optional, for advanced features)
