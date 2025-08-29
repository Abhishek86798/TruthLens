from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np
import logging

logger = logging.getLogger(__name__)

def test_model_performance():
    """Test model performance and analyze errors."""
    # Sample dataset
    texts = [
        "Global temperatures show clear warming trend according to NASA data",
        "Scientists confirm link between CO2 emissions and climate change",
        "No evidence supports climate change claims according to blog post",
        "Research paper demonstrates impact of human activity on climate",
        "Natural cycles explain all climate patterns claims social media",
        "Multiple studies confirm rising sea levels worldwide",
        "Climate scientists manipulate data to create panic",
        "Satellite data shows accelerating ice melt in polar regions",
        "Blog claims climate change is a hoax without evidence",
        "Peer-reviewed study shows increasing extreme weather events"
    ]

    labels = np.array([1, 1, 0, 1, 0, 1, 0, 1, 0, 1])  # 1: factual, 0: questionable
    label_names = ['Questionable', 'Factual']

    # Train and evaluate model
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.4, random_state=42
    )

    vectorizer = TfidfVectorizer(max_features=100)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    clf = LogisticRegression(random_state=42)
    clf.fit(X_train_tfidf, y_train)
    y_pred = clf.predict(X_test_tfidf)

    # Print results
    print("\n📊 Confusion Matrix")
    print("-" * 40)
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n{label_names[0]:>12} {label_names[1]:>12}")
    for i, row in enumerate(cm):
        print(f"{label_names[i]:>12}: {row[0]:>11} {row[1]:>12}")

    # Analyze errors
    print("\n❌ Misclassified Examples")
    print("-" * 40)
    for text, true, pred in zip(X_test, y_test, y_pred):
        if true != pred:
            print(f"\nText: {text}")
            print(f"True: {label_names[true]}")
            print(f"Predicted: {label_names[pred]}")

    # Show feature importance
    print("\n📈 Model Analysis")
    print("-" * 40)
    feature_names = vectorizer.get_feature_names_out()
    top_features = np.argsort(np.abs(clf.coef_[0]))[-5:]

    print("\nTop predictive words:")
    for idx in reversed(top_features):
        print(f"- {feature_names[idx]}")

if __name__ == "__main__":
    test_model_performance()
