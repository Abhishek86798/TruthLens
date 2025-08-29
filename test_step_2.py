import requests
import time
import random
import os
from typing import Optional
from langdetect import detect, DetectorFactory
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
import numpy as np

# Set seed for consistent results
DetectorFactory.seed = 0

def fetch_with_retry(url: str, max_retries: int = 3, base_delay: float = 1.0) -> Optional[requests.Response]:
    """
    Fetch URL with exponential backoff retry logic and jitter
    """
    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt + 1} of {max_retries}")
            response = requests.get(url)
            print(f"Status: {response.status_code}")
            return response
            
        except requests.RequestException as e:
            if attempt == max_retries - 1:  # Last attempt
                print(f"Final attempt failed: {str(e)}")
                return None
                
            # Calculate delay with exponential backoff and jitter
            delay = base_delay * (2 ** attempt)  # exponential backoff
            jitter = random.uniform(0, 0.1 * delay)  # 10% jitter
            total_delay = delay + jitter
            
            print(f"Request failed: {str(e)}")
            print(f"Retrying in {total_delay:.2f} seconds...")
            time.sleep(total_delay)

def detect_language(text: str) -> str:
    """
    Detect the language of given text.
    Returns ISO 639-1 language code.
    """
    try:
        return detect(text)
    except Exception as e:
        return f"Error: {str(e)}"

def create_annotation_guidelines() -> str:
    """
    Generate markdown-formatted annotation guidelines.
    """
    guidelines = """
# TruthLens Annotation Guidelines

## Overview
These guidelines help ensure consistent fact-checking annotations across the dataset.

## Label Definitions

### True (1.0)
- Claim is completely accurate
- All key facts are supported by reliable evidence
- No missing context that would change interpretation

✅ Example: "The average global temperature has risen by approximately 1°C since pre-industrial times."

### Partially True (0.5)
- Claim contains both accurate and inaccurate elements
- Important context is missing
- Oversimplified to point of misleading

⚠️ Example: "Social media causes depression in teenagers"
> Why partially true: While studies show correlation between social media use and depression, causation isn't definitively proven.

### False (0.0)
- Claim is demonstrably false
- Contradicts established evidence
- Based on debunked information

❌ Example: "5G networks spread viruses"

### Unverifiable
- Cannot be proven true or false with available evidence
- Subjective claims
- Future predictions

❓ Example: "Artificial intelligence will achieve consciousness by 2050"

## Evidence Requirements

1. Minimum Sources
   - At least 2 independent sources
   - Prefer primary sources over secondary
   - Check source credibility

2. Source Types (in order of preference)
   - Peer-reviewed research
   - Government/institutional data
   - Expert statements
   - Credible news reporting

3. Recency
   - Prefer sources from last 2 years
   - Historical claims may use older sources
   - Check for updated information

## Annotation Process

1. Read claim carefully
2. Gather evidence
3. Check source credibility
4. Assess completeness
5. Choose label
6. Document reasoning
7. Note confidence level

## Common Pitfalls

- Don't rely on single sources
- Watch for context manipulation
- Check date relevance
- Beware of correlation/causation confusion
- Consider cultural/geographic context

## Quality Control

- Document uncertainty
- Flag complex cases
- Maintain consistent standards
- Seek peer review for difficult cases
"""
    return guidelines

def train_test_model():
    """Train and evaluate a simple text classifier."""
    print("🔬 Text Classification Model Demo")
    print("=" * 40)
    
    # Get data (subset of categories for quick demo)
    categories = ['sci.med', 'sci.space', 'rec.sport.baseball']
    print(f"\nLoading {len(categories)} categories from 20 Newsgroups...")
    
    data = fetch_20newsgroups(
        subset='all',
        categories=categories,
        shuffle=True,
        random_state=42,
        remove=('headers', 'footers', 'quotes')
    )
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target,
        test_size=0.2,
        random_state=42
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Feature extraction
    print("\nExtracting TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        min_df=5,
        max_df=0.7,
        stop_words='english'
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Train model
    print("\nTraining Logistic Regression...")
    clf = LogisticRegression(
        max_iter=1000,
        multi_class='multinomial',
        random_state=42
    )
    
    clf.fit(X_train_tfidf, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test_tfidf)
    
    print("\n📊 Model Performance")
    print("-" * 20)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    print(f"Macro F1: {f1_score(y_test, y_pred, average='macro'):.3f}")
    
    print("\nDetailed Performance:")
    print(classification_report(
        y_test, y_pred,
        target_names=data.target_names,
        digits=3
    ))

if __name__ == "__main__":
    print("Testing retry mechanism with exponential backoff...")
    result = fetch_with_retry("https://example.com")
    
    if result:
        print(f"\nFinal result successful! Status code: {result.status_code}")
    else:
        print("\nAll attempts failed")
        
    # Test samples in different languages
    samples = {
        "English": "This is a sample text in English language.",
        "Spanish": "Este es un ejemplo de texto en español.",
        "French": "Ceci est un exemple de texte en français.",
        "German": "Dies ist ein Beispieltext in deutscher Sprache."
    }
    
    print("\nLanguage Detection Test")
    print("-" * 50)
    
    for name, text in samples.items():
        lang_code = detect_language(text)
        print(f"\nSample ({name}):")
        print(f"Text: {text}")
        print(f"Detected language code: {lang_code}")
    
    try:
        guidelines = create_annotation_guidelines()
        print("\nAnnotation Guidelines")
        print("-" * 50)
        print(guidelines)
        print("\n✅ Annotation guidelines generated successfully")
        
        train_test_model()
        
    finally:
        print("\nCleaning up test file...")
        os.remove(__file__)
