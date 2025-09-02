import json
from src.features import FeatureExtractor
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_feature_extraction():
    # Test data with known entities
    texts = [
        "Barack Obama was president of the United States",
        "Apple Inc. announced new products in California",
        "Scientists at NASA discovered water on Mars"
    ]
    
    extractor = FeatureExtractor()
    features, feature_names = extractor.extract_features(texts)
    
    # Verify features
    logger.info(f"Feature matrix shape: {features.shape}")
    logger.info("\nNamed Entity Features:")
    ner_indices = [i for i, name in enumerate(feature_names) if name.startswith('NER_')]
    for text_idx, text in enumerate(texts):
        ner_features = features[text_idx, ner_indices]
        logger.info(f"\nText: {text}")
        logger.info("Entities found: " + 
                   ", ".join(name for i, name in enumerate(feature_names) 
                           if name.startswith('NER_') and ner_features[i] > 0))

if __name__ == "__main__":
    # Install spacy model if not present
    import spacy.cli
    try:
        spacy.load('en_core_web_sm')
    except OSError:
        spacy.cli.download('en_core_web_sm')
    
    test_feature_extraction()
