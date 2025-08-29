from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

# Enhanced balanced dataset with source credibility
training_data = {
    'texts': [
        "Global temperatures have risen 1.1°C since pre-industrial era according to IPCC report",
        "NASA satellites confirm Arctic ice loss acceleration",
        "WHO research shows vaccine safety across large populations",
        "University study demonstrates correlation between emissions and warming",
        "Blog post claims climate change is hoax without evidence",
        "Social media user suggests conspiracy without sources",
        "Anonymous website disputes scientific consensus without data",
        "Fringe group makes extraordinary claims without peer review"
    ],
    'sources': [
        {'type': 'scientific_org', 'credibility': 0.9, 'peer_reviewed': True},
        {'type': 'government_org', 'credibility': 0.9, 'peer_reviewed': True},
        {'type': 'scientific_org', 'credibility': 0.9, 'peer_reviewed': True},
        {'type': 'academic', 'credibility': 0.8, 'peer_reviewed': True},
        {'type': 'blog', 'credibility': 0.2, 'peer_reviewed': False},
        {'type': 'social_media', 'credibility': 0.1, 'peer_reviewed': False},
        {'type': 'unknown', 'credibility': 0.0, 'peer_reviewed': False},
        {'type': 'advocacy_group', 'credibility': 0.3, 'peer_reviewed': False}
    ],
    'labels': [1, 1, 1, 1, 0, 0, 0, 0]  # Balanced true/false claims
}
