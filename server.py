from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from src.preprocessing import clean_text, validate_content
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Models
class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    label: str
    confidence: float
    metadata: Dict[str, Any]

# Initialize FastAPI with metadata
app = FastAPI(
    title="TruthLens API",
    description="Fact-checking and misinformation detection API",
    version="0.1.0"
)

@app.get("/")
async def root():
    """Root endpoint showing API information"""
    return {
        "name": "TruthLens API",
        "version": "0.1.0",
        "documentation": "/docs",
        "endpoints": {
            "GET /": "This info",
            "GET /health": "Health check",
            "POST /predict": "Make prediction"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Prediction endpoint"""
    try:
        # Process text
        cleaned_text = clean_text(request.text)
        
        # Check for credibility markers
        credibility_markers = ['data', 'study', 'research', 'nasa', 'evidence']
        has_credible_source = any(marker in cleaned_text.lower() for marker in credibility_markers)
        
        # Validate content
        is_valid, reasons = validate_content(cleaned_text, min_words=5)
        
        # Calculate confidence
        confidence = 0.85 if has_credible_source and is_valid else 0.65
        
        return PredictionResponse(
            label="FACTUAL" if has_credible_source and is_valid else "QUESTIONABLE",
            confidence=confidence,
            metadata={
                "word_count": len(cleaned_text.split()),
                "has_credible_source": has_credible_source,
                "validation_issues": reasons,
                "is_valid": is_valid
            }
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Start the server with instructions"""
    print("\n=== TruthLens API Server ===")
    print("\nServer running at: http://localhost:8001")
    print("\nAvailable endpoints:")
    print("- GET  /          : API information")
    print("- GET  /health    : Health check")
    print("- GET  /docs      : API documentation")
    print("- POST /predict   : Make prediction")
    
    uvicorn.run(app, host="127.0.0.1", port=8001)

if __name__ == "__main__":
    main()
