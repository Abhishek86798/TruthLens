import requests
import time
import random
import os
from typing import List, Dict, Any
from enum import Enum
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_random_user_agent() -> str:
    user_agents: List[str] = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]
    return random.choice(user_agents)

def fetch_with_rotation(url: str, delay: float = 2.0) -> None:
    for i in range(3):
        user_agent = get_random_user_agent()
        headers = {'User-Agent': user_agent}
        
        try:
            response = requests.get(url, headers=headers)
            print(f"\nRequest {i + 1}:")
            print(f"Status: {response.status_code}")
            print(f"User-Agent: {user_agent}")
        except requests.RequestException as e:
            print(f"\nRequest {i + 1} failed: {str(e)}")
        
        if i < 2:  # Don't sleep after last request
            print(f"Waiting {delay} seconds...")
            time.sleep(delay)

def remove_duplicates(texts: List[str]) -> List[str]:
    """
    Remove exact duplicate texts while preserving original order of first occurrence.
    """
    seen = set()
    result = []
    for text in texts:
        if text not in seen:
            seen.add(text)
            result.append(text)
    return result

class AnnotationLabel(Enum):
    TRUE = "true"
    PARTIALLY_TRUE = "partially_true"
    FALSE = "false"
    UNVERIFIABLE = "unverifiable"

def annotate_claim(claim: str) -> Dict[str, Any]:
    """
    Simulate user annotation input for a claim.
    In production, this would be replaced with actual user input.
    """
    # Simulate reviewing the claim and making a decision
    print(f"\nAnnotating claim: '{claim}'")
    print("-" * 50)
    print("1. TRUE")
    print("2. PARTIALLY_TRUE")
    print("3. FALSE")
    print("4. UNVERIFIABLE")
    
    # Simulate automatic selection for demo
    # In production, this would be: label = input("Select label (1-4): ")
    if "temperature" in claim.lower():
        label = AnnotationLabel.TRUE
        confidence = "high"
        sources = ["IPCC Report 2023", "NASA Global Temperature Data"]
    else:
        label = AnnotationLabel.UNVERIFIABLE
        confidence = "low"
        sources = ["No reliable sources found"]
    
    return {
        "claim": claim,
        "label": label.value,
        "confidence": confidence,
        "sources": sources,
        "timestamp": "2023-11-14T12:00:00Z"  # In production, use actual timestamp
    }

def train_and_save_model():
    """Train text classifier and save the model pipeline."""
    try:
        # Load data
        logger.info("Loading sample data...")
        categories = ['sci.med', 'sci.space', 'alt.atheism']
        data = fetch_20newsgroups(
            categories=categories,
            remove=('headers', 'footers', 'quotes')
        )
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            data.data, data.target, test_size=0.2, random_state=42
        )
        
        # Create pipeline
        logger.info("Building model pipeline...")
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                min_df=5,
                max_df=0.7,
                stop_words='english'
            )),
            ('classifier', LogisticRegression(
                max_iter=1000,
                multi_class='multinomial'
            ))
        ])
        
        # Train
        logger.info("Training model...")
        pipeline.fit(X_train, y_train)
        
        # Evaluate
        logger.info("Evaluating model...")
        y_pred = pipeline.predict(X_test)
        print("\nModel Performance:")
        print(classification_report(
            y_test, y_pred,
            target_names=data.target_names
        ))
        
        # Save model
        model_path = "trained_model.joblib"
        logger.info(f"Saving model to {model_path}...")
        joblib.dump(pipeline, model_path)
        
        # Test loading
        logger.info("Testing model loading...")
        loaded_model = joblib.load(model_path)
        test_pred = loaded_model.predict([data.data[0]])
        print(f"\nTest prediction successful: {data.target_names[test_pred[0]]}")
        
        # Cleanup model file
        os.remove(model_path)
        logger.info("Model file cleaned up")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise
    finally:
        if os.path.exists(model_path):
            os.remove(model_path)

if __name__ == "__main__":
    print("Testing user agent rotation with rate limiting...")
    fetch_with_rotation("https://example.com")
    
    print("\nTesting duplicate removal functionality...")
    sample_texts = [
        "This is the first text.",
        "This is another text.",
        "This is the first text.",  # Duplicate
        "This is unique text.",
        "This is another text.",    # Duplicate
        "Final unique text."
    ]
    
    print("Original texts:")
    print("-" * 50)
    for i, text in enumerate(sample_texts, 1):
        print(f"{i}. {text}")
    
    deduped_texts = remove_duplicates(sample_texts)
    
    print("\nAfter removing duplicates:")
    print("-" * 50)
    for i, text in enumerate(deduped_texts, 1):
        print(f"{i}. {text}")
    
    print(f"\nRemoved {len(sample_texts) - len(deduped_texts)} duplicates")
    
    try:
        train_and_save_model()
    finally:
        print("\nCleaning up test file...")
        os.remove(__file__)
