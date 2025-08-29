from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="TruthLens API")

class PredictionRequest(BaseModel):
    text: str = Field(..., description="Text to analyze")

class PredictionResponse(BaseModel):
    label: str
    confidence: float
    metadata: Dict[str, Any]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Mock prediction
        word_count = len(request.text.split())
        label = "FACTUAL" if word_count > 20 else "QUESTIONABLE"
        
        return PredictionResponse(
            label=label,
            confidence=0.85,
            metadata={
                "word_count": word_count,
                "text_length": len(request.text)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("\n=== TruthLens API Server ===")
    print("\nServer starting at http://localhost:8000")
    print("\nTest commands (run in a new PowerShell window):")
    print("\n1. Health check (copy and paste this command):")
    print('Invoke-RestMethod -Uri "http://localhost:8000/health"')
    print("\n2. Prediction test (copy and paste these commands):")
    print('$body = @{"text"="Global temperatures have risen significantly according to NASA data"}')
    print('$jsonBody = $body | ConvertTo-Json')
    print('Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $jsonBody -ContentType "application/json"')
    print("\nOr open in browser: http://localhost:8000/docs")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
    print("\n2. Make prediction:")
    print('$body = @{"text"="Global temperatures have risen significantly according to NASA data"}')
    print('$jsonBody = $body | ConvertTo-Json')
    print('Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $jsonBody -ContentType "application/json"')
    print("\n3. Or open in browser:")
    print("http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop server")
    print("=" * 50)
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
