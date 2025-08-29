from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI with proper metadata
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

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "TruthLens API",
        "version": "0.1.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a prediction on input text"""
    try:
        # Process text
        words = request.text.split()
        credibility_markers = ['data', 'nasa', 'study', 'research', 'evidence']
        has_credible_source = any(marker in request.text.lower() for marker in credibility_markers)
        
        # Determine label and confidence
        is_factual = has_credible_source and len(words) >= 5
        confidence = 0.85 if is_factual else 0.65
        
        return PredictionResponse(
            label="FACTUAL" if is_factual else "QUESTIONABLE",
            confidence=confidence,
            metadata={
                "word_count": len(words),
                "has_credible_source": has_credible_source,
                "processed_length": len(request.text)
            }
        )
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("\n=== TruthLens API Server ===")
    print("Available endpoints:")
    print("1. API docs:      http://localhost:8001/docs")
    print("2. Health check:  http://localhost:8001/health")
    print("3. Prediction:    http://localhost:8001/predict (POST)")
    uvicorn.run(app, host="127.0.0.1", port=8001)
