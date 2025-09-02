import json
import logging
from pathlib import Path
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score
import numpy as np
import pickle


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaselineClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            min_df=2,
            ngram_range=(1, 2),
            strip_accents='unicode'
        )
        self.model = LogisticRegression(
            random_state=42,
            class_weight='balanced',
            max_iter=1000,
            C=1.0
        )
        self.min_folds = 2  # Minimum required folds
    
    def train_and_evaluate(self, dataset_path: str, model_dir: str):
        """Train model and save metrics with adaptive k-fold cross-validation."""
        try:
            model_dir = Path(model_dir)
            model_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info("Loading dataset...")
            data = []
            with open(dataset_path) as f:
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))
            
            # Prepare data
            df = pd.DataFrame(data)
            X = df['text']
            y = df['label']
            
            # Additional preprocessing
            df['text'] = df['text'].str.lower()
            
            # Determine number of folds (minimum 2, maximum 5)
            min_samples_per_class = min(df['label'].value_counts())
            n_folds = max(self.min_folds, min(5, min_samples_per_class // 2))
            
            logger.info(f"Using {n_folds}-fold cross-validation based on data size")
            
            # Vectorize all text
            X_vec = self.vectorizer.fit_transform(X)
            
            # Use StratifiedKFold for balanced folds
            cv = StratifiedKFold(
                n_splits=n_folds,
                shuffle=True,
                random_state=42
            )
            
            # Update scoring parameters
            cv_results = cross_validate(
                self.model, X_vec, y,
                cv=cv,
                scoring={
                    'accuracy': 'accuracy',
                    'precision': make_scorer(precision_score, average='weighted', zero_division=0),
                    'recall': make_scorer(recall_score, average='weighted', zero_division=0),
                    'f1': make_scorer(f1_score, average='weighted', zero_division=0)
                },
                return_train_score=True
            )
            
            # Format metrics
            metrics = {
                'cross_validation': {
                    'fold_scores': {
                        'accuracy': cv_results['test_accuracy'].tolist(),
                        'precision': cv_results['test_precision'].tolist(),
                        'recall': cv_results['test_recall'].tolist(),
                        'f1': cv_results['test_f1'].tolist()
                    },
                    'mean_scores': {
                        'accuracy': float(np.mean(cv_results['test_accuracy'])),
                        'precision': float(np.mean(cv_results['test_precision'])),
                        'recall': float(np.mean(cv_results['test_recall'])),
                        'f1': float(np.mean(cv_results['test_f1'])),
                    },
                    'std_scores': {
                        'accuracy': float(np.std(cv_results['test_accuracy'])),
                        'precision': float(np.std(cv_results['test_precision'])),
                        'recall': float(np.std(cv_results['test_recall'])),
                        'f1': float(np.std(cv_results['test_f1'])),
                    }
                },
                'data_size': len(df),
                'n_folds': n_folds
            }
            
            # Train final model on full dataset
            logger.info("Training final model on full dataset...")
            self.model.fit(X_vec, y)
            
            self._save_outputs(metrics, model_dir)
            return metrics
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise
    
    def _save_outputs(self, metrics, model_dir):
        metrics_path = model_dir / "metrics.json"
        model_path = model_dir / "baseline.pkl"
        
        # Save metrics
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Save model
        with open(model_path, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'model': self.model
            }, f)
        
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Metrics saved to {metrics_path}")
        logger.info(f"Mean accuracy: {metrics['cross_validation']['mean_scores']['accuracy']:.3f}")

def main():
    dataset_path = "data/processed/dataset.jsonl"
    model_dir = "models"
    
    classifier = BaselineClassifier()
    metrics = classifier.train_and_evaluate(dataset_path, model_dir)
    
    print("\nEvaluation Metrics:")
    print("-" * 40)
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            print(f"{key}: {value:.3f}")
    
    print("\nResults Summary:")
    print(f"- Accuracy: {metrics['accuracy']:.3f}")
    print(f"- F1 Score: {metrics['f1']:.3f}")
    print(f"- Training Examples: {metrics['train_size']}")
    print(f"- Test Examples: {metrics['test_size']}")
    
    print("\nCross-Validation Results:")
    print("-" * 40)
    for metric in ['accuracy', 'precision', 'recall', 'f1']:
        mean = metrics['cross_validation']['mean_scores'][metric]
        std = metrics['cross_validation']['std_scores'][metric]
        print(f"{metric}: {mean:.3f} (±{std:.3f})")
    
    print("\nFold Scores:")
    for i, acc in enumerate(metrics['cross_validation']['fold_scores']['accuracy'], 1):
        print(f"Fold {i}: {acc:.3f}")

if __name__ == "__main__":
    main()
    print("\nCross-Validation Results:")
    print("-" * 40)
    for metric in ['accuracy', 'precision', 'recall', 'f1']:
        mean = metrics['cross_validation']['mean_scores'][metric]
        std = metrics['cross_validation']['std_scores'][metric]
        print(f"{metric}: {mean:.3f} (±{std:.3f})")
    
    print("\nFold Scores:")
    for i, acc in enumerate(metrics['cross_validation']['fold_scores']['accuracy'], 1):
        print(f"Fold {i}: {acc:.3f}")

if __name__ == "__main__":
    main()
