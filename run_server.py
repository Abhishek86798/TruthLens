from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import logging
from src.preprocessing import clean_text, validate_content

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="TruthLens API",
    description="Fact-checking and misinformation detection API",
    version="0.1.0"
)

class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    label: str
    confidence: float
    metadata: Dict[str, Any]

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # Clean and validate text
        cleaned_text = clean_text(request.text)
        is_valid, reasons = validate_content(cleaned_text, min_words=5)
        
        return {
            "label": "FACTUAL" if is_valid else "QUESTIONABLE",
            "confidence": 0.85 if is_valid else 0.65,
            "metadata": {
                "cleaned_length": len(cleaned_text),
                "validation_issues": reasons,
                "is_valid": is_valid
            }
        }
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def main():
    print("\n=== TruthLens API Server ===")
    print("\nTest commands (run in another PowerShell window):")
    print("\n1. Health check:")
    print('Invoke-RestMethod -Uri "http://localhost:8001/health"')
    print("\n2. Make prediction:")
    print('$body = @{ text = "Global temperatures have risen significantly according to NASA data" }')
    print('$jsonBody = $body | ConvertTo-Json')
    print('Invoke-RestMethod -Uri "http://localhost:8001/predict" -Method Post -Body $jsonBody -ContentType "application/json"\n')
    
    uvicorn.run(app, host="127.0.0.1", port=8001)

if __name__ == "__main__":
    main()
