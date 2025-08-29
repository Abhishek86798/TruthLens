from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import shap
import numpy as np
import matplotlib.pyplot as plt
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_model_interpretability():
    """Test SHAP explanations for model predictions."""
    try:
        # Simple test dataset
        texts = [
            "The Earth is warming due to greenhouse gas emissions",
            "Scientists have documented rising global temperatures",
            "There is no evidence of climate change",
            "Data shows increasing ocean temperatures",
            "Natural cycles explain all climate patterns"
        ]
        labels = np.array([1, 1, 0, 1, 0])  # 1: factual, 0: questionable
        
        # Train simple pipeline
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=20)),
            ('clf', LogisticRegression())
        ])
        
        logger.info("Training model...")
        pipeline.fit(texts, labels)
        
        # Get feature names and matrix
        vectorizer = pipeline.named_steps['tfidf']
        feature_matrix = vectorizer.transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # Create SHAP explainer
        logger.info("Creating SHAP explainer...")
        explainer = shap.LinearExplainer(
            pipeline.named_steps['clf'],
            feature_matrix
        )
        
        # Get SHAP values
        shap_values = explainer.shap_values(feature_matrix)
        
        # Print feature importance
        print("\nTop Important Features:")
        print("-" * 20)
        importance = np.abs(shap_values).mean(0)
        for idx in np.argsort(-importance)[:5]:
            print(f"{feature_names[idx]}: {importance[idx]:.4f}")
        
        print("\n✅ SHAP analysis successful")
        return True
        
    except Exception as e:
        logger.error(f"SHAP analysis failed: {e}")
        return False

if __name__ == "__main__":
    success = test_model_interpretability()
    if not success:
        print("\n❌ Test failed - see logs for details")
