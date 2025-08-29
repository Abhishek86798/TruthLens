#!/usr/bin/env python3
"""
TruthLens API - Demo Version for Quick Deployment
Simplified version without heavy ML dependencies
"""

import os
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TruthLens API - Demo",
    description="AI-powered fact-checking API - Demo Version",
    version="1.0.0-demo"
)

# Pydantic models
class ClaimInput(BaseModel):
    claim: str
    context: Optional[str] = "Demo claim verification"

class VerificationResponse(BaseModel):
    claim: str
    verdict: str
    confidence: float
    reasoning: str
    sources_checked: list
    verification_badge: str
    evidence_strength: str
    stance_distribution: Dict[str, int]
    stance_percentages: Dict[str, float]
    fact_check_result: Optional[Dict[str, Any]]
    details: list
    processing_time: float
    timestamp: str
    total_articles: int
    source_breakdown: Dict[str, int]
    evidence_summary: str
    rule_based_overrides: list

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str
    version: str

# API Keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_news_articles(claim: str, max_articles: int = 5) -> list:
    """Get news articles from News API"""
    articles = []
    
    if not NEWS_API_KEY:
        logger.warning("News API key not configured")
        return articles
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": claim,
            "apiKey": NEWS_API_KEY,
            "pageSize": max_articles,
            "language": "en",
            "sortBy": "relevancy"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            logger.info(f"Found {len(articles)} news articles")
        
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
    
    return articles

def get_guardian_articles(claim: str, max_articles: int = 5) -> list:
    """Get articles from Guardian API"""
    articles = []
    
    if not GUARDIAN_API_KEY:
        logger.warning("Guardian API key not configured")
        return articles
    
    try:
        url = "https://content.guardianapis.com/search"
        params = {
            "q": claim,
            "api-key": GUARDIAN_API_KEY,
            "page-size": max_articles,
            "show-fields": "headline,bodyText,byline,publication,lastModified"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get("response", {}).get("status") == "ok":
            guardian_articles = data.get("response", {}).get("results", [])
            
            # Convert Guardian format to standard format
            for article in guardian_articles:
                articles.append({
                    "title": article.get("webTitle", ""),
                    "description": article.get("fields", {}).get("bodyText", "")[:200] + "...",
                    "url": article.get("webUrl", ""),
                    "source": {"name": "The Guardian"},
                    "publishedAt": article.get("webPublicationDate", ""),
                    "content": article.get("fields", {}).get("bodyText", "")
                })
            
            logger.info(f"Found {len(articles)} Guardian articles")
        
    except Exception as e:
        logger.error(f"Error fetching Guardian articles: {e}")
    
    return articles

def get_google_factcheck(claim: str) -> Optional[Dict[str, Any]]:
    """Get fact-check results from Google Fact Check API"""
    
    if not GOOGLE_API_KEY:
        logger.warning("Google API key not configured")
        return None
    
    try:
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {
            "query": claim,
            "key": GOOGLE_API_KEY,
            "maxAgeDays": 365
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        claims = data.get("claims", [])
        
        if claims:
            claim_data = claims[0]
            review = claim_data.get("claimReview", [{}])[0]
            
            return {
                "claim_text": claim_data.get("text", ""),
                "verdict": review.get("textualRating", "Unknown"),
                "confidence": 0.8,
                "sources": [review.get("publisher", {}).get("name", "")],
                "best_source": review.get("publisher", {}).get("name", ""),
                "review_date": review.get("reviewDate", ""),
                "explanation": review.get("textualRating", ""),
                "rating": review.get("textualRating", ""),
                "url": review.get("url", "")
            }
        
    except Exception as e:
        logger.error(f"Error fetching Google fact-check: {e}")
    
    return None

def analyze_claim_simple(claim: str, articles: list) -> Dict[str, Any]:
    """Simple claim analysis without heavy ML"""
    
    # Simple keyword-based analysis
    claim_lower = claim.lower()
    
    # Check for common false claim patterns
    false_patterns = [
        "flat earth", "moon landing fake", "vaccines cause autism",
        "climate change hoax", "5g coronavirus", "chemtrails"
    ]
    
    is_likely_false = any(pattern in claim_lower for pattern in false_patterns)
    
    # Simple stance analysis based on article titles
    support_count = 0
    contradict_count = 0
    neutral_count = 0
    
    for article in articles:
        title = article.get("title", "").lower()
        if any(word in title for word in ["true", "confirmed", "verified", "fact"]):
            support_count += 1
        elif any(word in title for word in ["false", "debunked", "hoax", "fake"]):
            contradict_count += 1
        else:
            neutral_count += 1
    
    total_articles = len(articles)
    if total_articles > 0:
        support_pct = support_count / total_articles
        contradict_pct = contradict_count / total_articles
        neutral_pct = neutral_count / total_articles
    else:
        support_pct = contradict_pct = neutral_pct = 0
    
    # Determine verdict
    if is_likely_false:
        verdict = "Likely False"
        confidence = 0.85
        reasoning = "Claim matches known false claim patterns"
    elif contradict_count > support_count:
        verdict = "Likely False"
        confidence = 0.7
        reasoning = "More contradicting articles found"
    elif support_count > contradict_count:
        verdict = "Likely True"
        confidence = 0.7
        reasoning = "More supporting articles found"
    else:
        verdict = "Uncertain"
        confidence = 0.5
        reasoning = "Mixed evidence found"
    
    return {
        "verdict": verdict,
        "confidence": confidence,
        "reasoning": reasoning,
        "stance_distribution": {
            "support": support_count,
            "contradict": contradict_count,
            "neutral": neutral_count
        },
        "stance_percentages": {
            "support": support_pct,
            "contradict": contradict_pct,
            "neutral": neutral_pct
        }
    }

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "TruthLens API - Demo Version",
        "status": "running",
        "version": "1.0.0-demo"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="TruthLens API is running",
        timestamp=datetime.now().isoformat(),
        version="1.0.0-demo"
    )

@app.post("/verify", response_model=VerificationResponse)
async def verify_claim(claim_input: ClaimInput):
    """Verify a claim using available sources"""
    
    start_time = time.time()
    
    try:
        # Get news articles
        news_articles = get_news_articles(claim_input.claim, max_articles=3)
        guardian_articles = get_guardian_articles(claim_input.claim, max_articles=3)
        
        # Combine articles
        all_articles = news_articles + guardian_articles
        
        # Get fact-check results
        fact_check = get_google_factcheck(claim_input.claim)
        
        # Analyze claim
        analysis = analyze_claim_simple(claim_input.claim, all_articles)
        
        # Prepare response
        processing_time = time.time() - start_time
        
        # Convert articles to response format
        article_details = []
        for article in all_articles[:5]:  # Limit to 5 articles
            article_details.append({
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "source_name": "NewsAPI" if article in news_articles else "Guardian",
                "similarity_score": 0.5,  # Placeholder
                "published_at": article.get("publishedAt", ""),
                "relevance_score": 0.5,  # Placeholder
                "stance": "neutral",  # Placeholder
                "stance_confidence": 0.5  # Placeholder
            })
        
        # Source breakdown
        source_breakdown = {
            "NewsAPI": len(news_articles),
            "Guardian": len(guardian_articles)
        }
        
        return VerificationResponse(
            claim=claim_input.claim,
            verdict=analysis["verdict"],
            confidence=analysis["confidence"],
            reasoning=analysis["reasoning"],
            sources_checked=["News API", "Guardian API"],
            verification_badge="🔍 Demo Analysis",
            evidence_strength="Medium" if len(all_articles) > 2 else "Weak",
            stance_distribution=analysis["stance_distribution"],
            stance_percentages=analysis["stance_percentages"],
            fact_check_result=fact_check,
            details=article_details,
            processing_time=processing_time,
            timestamp=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            total_articles=len(all_articles),
            source_breakdown=source_breakdown,
            evidence_summary=f"Found {len(all_articles)} articles",
            rule_based_overrides=[]
        )
        
    except Exception as e:
        logger.error(f"Error in claim verification: {e}")
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@app.get("/components-status")
async def components_status():
    """Check status of API components"""
    return {
        "status": "demo_mode",
        "components": {
            "news_api": "available" if NEWS_API_KEY else "not_configured",
            "guardian_api": "available" if GUARDIAN_API_KEY else "not_configured",
            "google_factcheck": "available" if GOOGLE_API_KEY else "not_configured",
            "ml_models": "disabled_demo_mode"
        },
        "message": "Running in demo mode - limited functionality"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
