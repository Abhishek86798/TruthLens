import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class FeatureExtractor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.entity_types = ['PERSON', 'ORG', 'GPE', 'DATE', 'NORP']
        self.pos_tags = ['NOUN', 'VERB', 'ADJ', 'ADV']
    
    def extract_features(self, texts: List[str]) -> Tuple[np.ndarray, List[str]]:
        """Extract TF-IDF, NER, and POS features."""
        # Basic TF-IDF features
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        feature_names = list(self.vectorizer.get_feature_names_out())
        
        # Extract NER and POS features
        ner_features = []
        pos_features = []
        
        for text in texts:
            doc = self.nlp(text)
            
            # NER features
            entities = {ent_type: 0 for ent_type in self.entity_types}
            for ent in doc.ents:
                if ent.label_ in entities:
                    entities[ent.label_] = 1
            
            # POS features
            pos_counts = {tag: 0 for tag in self.pos_tags}
            for token in doc:
                if token.pos_ in pos_counts:
                    pos_counts[token.pos_] = 1
            
            ner_features.append(list(entities.values()))
            pos_features.append(list(pos_counts.values()))
        
        # Combine all features
        ner_matrix = np.array(ner_features)
        pos_matrix = np.array(pos_features)
        
        combined_matrix = np.hstack([
            tfidf_matrix.toarray(),
            ner_matrix,
            pos_matrix
        ])
        
        # Add feature names
        feature_names.extend([f'NER_{ent}' for ent in self.entity_types])
        feature_names.extend([f'POS_{tag}' for tag in self.pos_tags])
        
        return combined_matrix, feature_names
