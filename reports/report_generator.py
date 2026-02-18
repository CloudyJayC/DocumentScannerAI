
# Report generation for DocumentScannerAI
# Outputs a clean, well-structured text report summarizing the analysis results.

from datetime import datetime

def generate_text_report(file_path, suspicious, keyword_results, ai_results, output_path=None):
	"""
	Generate a readable text report of the PDF analysis.
	Args:
		file_path: Path to the analyzed PDF file
		suspicious: dict of suspicious PDF elements
		keyword_results: dict from analyze_keywords
		ai_results: dict from ai_analyze_text
		output_path: Optional path to save the report (default: <file_path>_report.txt)
	Returns: The path to the saved report file.
	"""
	if output_path is None:
		output_path = file_path + "_report.txt"
	with open(output_path, 'w', encoding='utf-8') as f:
		f.write(f"DocumentScannerAI Report\n")
		f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
		f.write(f"Analyzed File: {file_path}\n\n")

		f.write("--- Security Scan ---\n")
		if any(count > 0 for count in suspicious.values()):
			f.write("Suspicious PDF Elements Detected:\n")
			for element, count in suspicious.items():
				if count > 0:
					f.write(f"  {element}: {count}\n")
		else:
			f.write("No suspicious elements found. File is clean.\n")
		f.write("\n")

		f.write("--- Keyword Analysis ---\n")
		f.write(f"Word count: {keyword_results['word_count']}\n")
		f.write(f"Unique words: {keyword_results['unique_words']}\n")
		f.write("Top keywords:\n")
		for word, freq in keyword_results['keywords']:
			f.write(f"  {word}: {freq}\n")
		f.write("\n")

		f.write("--- AI-Powered Entity Analysis ---\n")
		if 'error' in ai_results:
			f.write(f"AI Analysis Error: {ai_results['error']}\n")
		else:
			f.write("Summary (first 3 sentences):\n")
			f.write(ai_results['summary'] + "\n\n")
			grouped = ai_results.get('entities_grouped', {})
			if grouped:
				# Write grouped entities with explanations
				label_explanations = {
					'PERSON': 'People found in the document:',
					'ORG': 'Organizations/Companies:',
					'GPE': 'Locations:',
					'DATE': 'Dates:',
					'PERCENT': 'Percentages:',
					'CARDINAL': 'Numbers:',
					'LAW': 'Legal references:',
					'NORP': 'Nationalities or religious/political groups:',
				}
				for label, ents in grouped.items():
					if not ents:
						continue
					explanation = label_explanations.get(label, f"Other ({label}):")
					f.write(f"{explanation}\n")
					for ent in sorted(set(ents)):
						f.write(f"  - {ent}\n")
					f.write("\n")
			else:
				f.write("No named entities found.\n")
	return output_path
