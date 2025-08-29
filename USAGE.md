# TruthLens Usage Guide

## 1. Initial Setup

```powershell
# Install required packages
pip install -r requirements.txt

# Setup DVC
python setup_dvc.py
```

## 2. Data Collection

```python
# Async data collection
from src.data_collection import collect_from_urls

urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]

async def fetch_data():
    results = await collect_from_urls(urls, concurrency=5)
    return results

# Run with:
import asyncio
results = asyncio.run(fetch_data())
```

## 3. Text Processing

```python
from src.preprocessing import clean_html, normalize_text, validate_text, enrich_text

# Clean and process text
html_content = "<html>Your content here</html>"
cleaned = clean_html(html_content)
normalized = normalize_text(cleaned)

# Validate content
is_valid, reason = validate_text(normalized)

# Get text features
features = enrich_text(normalized)
```

## 4. Dataset Versioning

```powershell
# Initialize versioning
python init_dataset.py

# Save new version
python version_dataset.py
```

## 5. Annotation

```python
from src.annotation import AnnotationManager

# Initialize annotation manager
am = AnnotationManager()

# Save annotation
annotation = {
    "id": "doc1",
    "text": "Sample text",
    "label": "RELIABLE",
    "annotator": "user1"
}
am.save_annotation(annotation)
```

## 6. Quality Checks

```python
from src.preprocessing import check_data_quality

# Check dataset quality
quality_report = check_data_quality(dataset)
print(f"Quality Score: {quality_report['quality_score']}")
```
