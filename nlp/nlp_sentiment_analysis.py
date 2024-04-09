import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def load_reviews(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_reviews_with_score(reviews: dict, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

def preprocess_text(text: str) -> str:
    tokens = word_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    return ' '.join(tokens)

def calculate_drm_relevance(text: str, drm_keywords: list) -> float:
    words = text.split()
    drm_count = sum(text.count(word) for word in drm_keywords)
    total_count = len(words)
    return drm_count / total_count if total_count > 0 else 0

def analyze_reviews_for_drm(reviews: dict) -> dict:
    drm_keywords = [
        'drm', 'digital rights', 'copy', 'share', 'restrict', 'license', 
        'activation', 'print', 'authorization', 'locked', 'protected', 
        'playback', 'download', 'device', 'denied', 'region', 
        'limit', 'encryption', 'unauthorized', 'unavailable', 
        'authentication', 'not playable', 'not opening', 'access',
        'difficult', 'unusable', 'unintuitive'
    ]
    
    analyzed_reviews = {}
    max_score = 0
    for app, app_reviews in reviews.items():
        for review in app_reviews:
            review_text = preprocess_text(review['title'] + ' ' + review['body'])
            score = calculate_drm_relevance(review_text, drm_keywords)
            max_score = max(max_score, score)
            review['drm_relevance'] = score
            if app not in analyzed_reviews:
                analyzed_reviews[app] = []
            analyzed_reviews[app].append(review)

    # Normalize scores
    if max_score > 0:
        for app_reviews in analyzed_reviews.values():
            for review in app_reviews:
                review['drm_relevance'] /= max_score

    return analyzed_reviews