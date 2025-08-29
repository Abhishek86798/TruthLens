from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TruthLens Metrics")

# Define metrics
REQUEST_COUNT = Counter(
    'truthlens_requests_total',
    'Total requests by endpoint',
    ['endpoint']
)

REQUEST_LATENCY = Histogram(
    'truthlens_request_duration_seconds',
    'Request duration in seconds',
    ['endpoint']
)

class PredictRequest(BaseModel):
    text: str

@app.get("/health")
async def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()
    return {"status": "healthy"}

@app.post("/predict")
async def predict(request: PredictRequest):
    start_time = time.time()
    REQUEST_COUNT.labels(endpoint="/predict").inc()
    
    # Enhanced prediction logic
    words = request.text.split()
    credibility_markers = ['data', 'study', 'research', 'evidence', 'scientists', 'nasa', 'report']
    has_credible_source = any(marker in request.text.lower() for marker in credibility_markers)
    
    # Score based on multiple factors
    word_count = len(words)
    has_sufficient_length = word_count >= 8
    
    is_factual = has_credible_source and has_sufficient_length
    confidence = 0.85 if is_factual else 0.65
    
    REQUEST_LATENCY.labels(endpoint="/predict").observe(time.time() - start_time)
    
    return {
        "label": "FACTUAL" if is_factual else "QUESTIONABLE",
        "confidence": confidence,
        "metadata": {
            "word_count": word_count,
            "has_credible_source": has_credible_source,
            "processing_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    }

@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    logger.info("Starting server with metrics...")
    logger.info("Test with these PowerShell commands:")
    logger.info('1. Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get')
    logger.info('2. $body = @{"text"="Global temperatures have risen significantly according to NASA data"}')
    logger.info('3. Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body ($body | ConvertTo-Json) -ContentType "application/json"')
    logger.info('4. Invoke-RestMethod -Uri "http://localhost:8000/metrics" -Method Get')
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
