from fastapi import FastAPI, Query
from pydantic import BaseModel
import uvicorn
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="TruthLens API Viewer",
    description="View and test TruthLens API endpoints",
    version="0.1.0"
)

class FactCheckRequest(BaseModel):
    text: str

class FactCheckResponse(BaseModel):
    label: str
    confidence: float
    metadata: dict

@app.get("/")
async def root():
    return {
        "message": "Welcome to TruthLens API",
        "endpoints": {
            "Swagger UI": "/docs",
            "Health Check": "/health",
            "Predict": "/predict"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/predict")
async def predict(request: FactCheckRequest):
    return {
        "label": "FACTUAL" if len(request.text.split()) > 20 else "QUESTIONABLE",
        "confidence": 0.85,
        "metadata": {
            "word_count": len(request.text.split())
        }
    }

def main():
    logger.info("\n=== TruthLens API Server ===")
    logger.info("\nAvailable URLs:")
    logger.info("1. Main page:     http://localhost:8000/")
    logger.info("2. API docs:      http://localhost:8000/docs")
    logger.info("3. Health check:  http://localhost:8000/health")
    logger.info("\nTest commands (in another PowerShell window):")
    logger.info("\n# Health check:")
    logger.info('Invoke-RestMethod -Uri "http://localhost:8000/health"')
    logger.info("\n# Prediction:")
    logger.info('$body = @{ text = "Global temperatures have risen significantly according to NASA data" }')
    logger.info('$jsonBody = $body | ConvertTo-Json')
    logger.info('Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $jsonBody -ContentType "application/json"')
    
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
