import logging
import requests
import os
from datetime import datetime
from readability import Document
from typing import List, Dict, Any
import json
from enum import Enum
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report, roc_curve
)
import matplotlib.pyplot as plt
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'truthlens_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)

logger = logging.getLogger(__name__)

def fetch_with_logging(url: str) -> None:
    logger.info(f"Starting request to {url}")
    
    try:
        response = requests.get(url)
        logger.info(f"Request successful - Status code: {response.status_code}")
        
    except requests.RequestException as e:
        logger.error(f"Request failed: {str(e)}", exc_info=True)
        
    logger.info("Request attempt completed")

def extract_main_content(html: str) -> tuple[str, str]:
    """
    Extract main content from HTML, removing boilerplate.
    Returns tuple of (title, main_content)
    """
    doc = Document(html)
    title = doc.title()
    content = doc.summary()
    return title, content

class Label(Enum):
    TRUE = "true"
    PARTIALLY_TRUE = "partially_true"
    FALSE = "false"
    UNVERIFIABLE = "unverifiable"

def create_sample_dataset() -> List[Dict[str, Any]]:
    """Create a sample annotated dataset."""
    dataset = [
        {
            "id": "claim_001",
            "text": "Global temperatures have risen by 1.1°C since pre-industrial times",
            "label": Label.TRUE.value,
            "confidence": "high",
            "sources": ["IPCC Report 2023", "NASA Climate Data"],
            "annotator": "expert_1",
            "timestamp": "2023-11-14T10:00:00Z"
        },
        {
            "id": "claim_002",
            "text": "Social media is the leading cause of depression in teenagers",
            "label": Label.PARTIALLY_TRUE.value,
            "confidence": "medium",
            "sources": ["Research Paper 2022", "WHO Report"],
            "annotator": "expert_2",
            "timestamp": "2023-11-14T10:15:00Z"
        },
        {
            "id": "claim_003",
            "text": "5G networks spread viruses",
            "label": Label.FALSE.value,
            "confidence": "high",
            "sources": ["WHO Statement", "Scientific Studies"],
            "annotator": "expert_1",
            "timestamp": "2023-11-14T10:30:00Z"
        },
        {
            "id": "claim_004",
            "text": "Artificial intelligence will achieve consciousness by 2050",
            "label": Label.UNVERIFIABLE.value,
            "confidence": "low",
            "sources": ["Expert Opinions"],
            "annotator": "expert_2",
            "timestamp": "2023-11-14T10:45:00Z"
        }
    ]
    return dataset

def evaluate_model():
    """Train a classifier and evaluate with multiple metrics."""
    print("📊 Model Evaluation Metrics Demo")
    print("=" * 40)
    
    # Generate sample dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_classes=2,
        n_informative=15,
        random_state=42
    )
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    clf = LogisticRegression(random_state=42)
    clf.fit(X_train, y_train)
    
    # Get predictions
    y_pred = clf.predict(X_test)
    y_pred_proba = clf.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    print("\nClassification Metrics:")
    print("-" * 25)
    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "ROC AUC": roc_auc_score(y_test, y_pred_proba)
    }
    
    for metric_name, value in metrics.items():
        print(f"{metric_name}: {value:.3f}")
    
    # Print confusion matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Detailed classification report
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Plot ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
             label=f'ROC curve (AUC = {metrics["ROC AUC"]:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.savefig('roc_curve.png')
    plt.close()
    
    print("\nROC curve saved as 'roc_curve.png'")

if __name__ == "__main__":
    logger.info("=== Starting test script ===")
    fetch_with_logging("https://example.com")
    logger.info("=== Test script completed ===")
    
    # Test sample with boilerplate
    sample_html = """
    <html>
        <head><title>Test Article</title></head>
        <body>
            <nav>
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                </ul>
            </nav>
            
            <div class="ads">
                <p>Advertisement content here</p>
            </div>
            
            <article>
                <h1>Main Article Title</h1>
                <p>This is the actual main content that we want to extract.</p>
                <p>It contains multiple paragraphs of real content.</p>
            </article>
            
            <footer>
                <p>Copyright 2023</p>
                <p>More navigation links</p>
            </footer>
        </body>
    </html>
    """
    
    logger.info("Extracting main content from HTML...")
    logger.info("-" * 50)
    
    title, main_content = extract_main_content(sample_html)
    
    logger.info(f"\nExtracted Title: {title}")
    logger.info("\nExtracted Main Content:")
    logger.info("-" * 50)
    logger.info(main_content)
    
    logger.info("Creating sample dataset...")
    dataset = create_sample_dataset()
    
    logger.info("📊 TruthLens Annotated Dataset Summary")
    logger.info("=" * 40)
    
    # Dataset statistics
    label_counts = {}
    confidence_levels = {}
    
    for item in dataset:
        label_counts[item['label']] = label_counts.get(item['label'], 0) + 1
        confidence_levels[item['confidence']] = confidence_levels.get(item['confidence'], 0) + 1
    
    logger.info(f"Total examples: {len(dataset)}")
    logger.info("\nLabel distribution:")
    for label, count in label_counts.items():
        logger.info(f"- {label}: {count}")
        
    logger.info("\nConfidence distribution:")
    for conf, count in confidence_levels.items():
        logger.info(f"- {conf}: {count}")
    
    logger.info("\nSample entry:")
    logger.info(json.dumps(dataset[0], indent=2))
    
    logger.info("Cleaning up test file...")
    os.remove(__file__)

    try:
        evaluate_model()
    finally:
        # Cleanup
        print("\nCleaning up files...")
        if os.path.exists('roc_curve.png'):
            os.remove('roc_curve.png')
        os.remove(__file__)
