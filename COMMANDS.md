# TruthLens Command Reference

## Initial Setup

```powershell
# 1. Install core dependencies
pip install aiohttp tenacity beautifulsoup4 nltk textstat fastapi uvicorn

# 2. Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"

# 3. Setup DVC (one time)
python setup_dvc.py
```

## Running Components

### 1. Web Server

```powershell
# Start API server
python server.py
```

### 2. Test Endpoints

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8001/health"

# Make prediction
$body = @{
    text = "Global temperatures have risen significantly according to NASA data"
}
$jsonBody = $body | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8001/predict" -Method Post -Body $jsonBody -ContentType "application/json"
```

### 3. Data Processing

```powershell
# Run preprocessing tests
python test_preprocessing.py

# Test data collection
python test_scraper.py

# Test enrichment
python test_enrichment.py
```

### 4. Dataset Versioning

```powershell
# Initialize dataset
python init_dataset.py

# Save new version
python version_dataset.py
```

### 5. Development Tools

```powershell
# Run all tests
python -m pytest tests/

# Check data quality
python -c "from src.preprocessing import check_data_quality; print(check_data_quality(dataset))"
```

## Common Issues

### Port in Use

```powershell
# Find process using port 8001
netstat -ano | findstr :8001

# Kill process
taskkill /PID <PID> /F
```

### Reset DVC

```powershell
# Clean and reinitialize DVC
python reset_dvc.py
```

### Clean Environment

```powershell
# Remove cached files
Remove-Item -Recurse -Force __pycache__/
Remove-Item -Recurse -Force .pytest_cache/
```

## 7. Development Tools

```powershell
# Install dependencies
pip install -r requirements.txt

# Update dependencies
pip freeze > requirements.txt
```

## Common Issues

1. Port already in use:

```powershell
# Kill process using port 8001
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

2. Reset database:

```powershell
# Remove and recreate database
Remove-Item truthlens.db
python init_db.py
```

## Environment Setup

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install development requirements
pip install -r requirements-dev.txt
```
