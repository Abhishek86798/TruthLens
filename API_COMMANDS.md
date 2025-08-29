# TruthLens API Commands

## 1. Start Server
```powershell
# Start the API server
cd C:\TruthLens
python server.py
```

## 2. Test Endpoints

### Health Check
```powershell
# Simple health check
Invoke-RestMethod -Uri "http://localhost:8001/health"
```

### Root Endpoint
```powershell
# Get API information
Invoke-RestMethod -Uri "http://localhost:8001/"
```

### Prediction Endpoint
```powershell
# Define prediction request
$body = @{
    text = "Global temperatures have risen significantly according to NASA data"
}
$jsonBody = $body | ConvertTo-Json

# Make prediction
Invoke-RestMethod -Uri "http://localhost:8001/predict" -Method Post -Body $jsonBody -ContentType "application/json"
```

## 3. Sample Predictions

### Factual Example
```powershell
$body = @{
    text = "According to NASA research data, global temperatures have shown a significant rise over the past century, with multiple independent studies confirming this trend."
}
$jsonBody = $body | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8001/predict" -Method Post -Body $jsonBody -ContentType "application/json"
```

### Questionable Example
```powershell
$body = @{
    text = "Climate change is not real"
}
$jsonBody = $body | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8001/predict" -Method Post -Body $jsonBody -ContentType "application/json"
```

## 4. Browser Access
- API Documentation: http://localhost:8001/docs
- OpenAPI Schema: http://localhost:8001/openapi.json
