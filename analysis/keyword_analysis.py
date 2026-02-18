# Keyword and skill extraction logic
# Analyzes text for most frequent keywords, excluding common stopwords.
from collections import Counter
import string

def analyze_keywords(text):
    """
    Returns a dict with:
      - keywords: list of (word, frequency) tuples (top 10)
      - word_count: total number of words
      - unique_words: number of unique non-stopword words
    """
    # Remove punctuation and convert to lowercase
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    # Remove common stopwords
    stopwords = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'with', 'for', 'as', 'on', 'are', 'by', 'this', 'be'}
    filtered_words = [w for w in words if w not in stopwords]
    # Count word frequencies
    counter = Counter(filtered_words)
    keywords = counter.most_common(10)
    return {
        'keywords': keywords,
        'word_count': len(words),
        'unique_words': len(set(filtered_words))
    }
