#!/usr/bin/env python3
"""
TruthLens Streamlit Demo Interface
A user-friendly web interface for fact-checking claims
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TruthLens - AI Fact Checker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .verdict-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .verdict-true {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .verdict-false {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .verdict-uncertain {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .article-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def verify_claim(claim, context=""):
    """Send claim verification request to API"""
    try:
        payload = {
            "claim": claim,
            "context": context or "Streamlit demo verification"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/verify",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection Error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected Error: {str(e)}"}

def get_verdict_color(verdict):
    """Get color class for verdict"""
    if "true" in verdict.lower():
        return "verdict-true"
    elif "false" in verdict.lower():
        return "verdict-false"
    else:
        return "verdict-uncertain"

def display_verdict(result):
    """Display the verification verdict"""
    verdict = result.get("verdict", "Unknown")
    confidence = result.get("confidence", 0)
    
    st.markdown(f"""
    <div class="verdict-box {get_verdict_color(verdict)}">
        <h2>🔍 Verdict: {verdict}</h2>
        <p><strong>Confidence:</strong> {confidence:.1%}</p>
        <p><strong>Reasoning:</strong> {result.get('reasoning', 'No reasoning provided')}</p>
    </div>
    """, unsafe_allow_html=True)

def display_metrics(result):
    """Display key metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Articles Found",
            result.get("total_articles", 0),
            help="Total number of articles analyzed"
        )
    
    with col2:
        st.metric(
            "Processing Time",
            f"{result.get('processing_time', 0):.2f}s",
            help="Time taken to verify the claim"
        )
    
    with col3:
        evidence_strength = result.get("evidence_strength", "Unknown")
        st.metric(
            "Evidence Strength",
            evidence_strength,
            help="Strength of evidence found"
        )
    
    with col4:
        sources = len(result.get("sources_checked", []))
        st.metric(
            "Sources Used",
            sources,
            help="Number of sources checked"
        )

def display_stance_analysis(result):
    """Display stance analysis"""
    stance_dist = result.get("stance_distribution", {})
    stance_pct = result.get("stance_percentages", {})
    
    if stance_dist:
        st.subheader("📊 Stance Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Supporting",
                stance_dist.get("support", 0),
                f"{stance_pct.get('support', 0):.1%}"
            )
        
        with col2:
            st.metric(
                "Contradicting",
                stance_dist.get("contradict", 0),
                f"{stance_pct.get('contradict', 0):.1%}"
            )
        
        with col3:
            st.metric(
                "Neutral",
                stance_dist.get("neutral", 0),
                f"{stance_pct.get('neutral', 0):.1%}"
            )

def display_articles(result):
    """Display found articles"""
    details = result.get("details", [])
    
    if details:
        st.subheader("📰 Related Articles")
        
        for i, article in enumerate(details[:5]):  # Show first 5 articles
            with st.expander(f"Article {i+1}: {article.get('title', 'No title')[:50]}..."):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Title:** {article.get('title', 'No title')}")
                    st.write(f"**Source:** {article.get('source', 'Unknown')}")
                    st.write(f"**Published:** {article.get('published_at', 'Unknown')}")
                    
                    if article.get('url'):
                        st.write(f"**URL:** [{article.get('url', '')}]({article.get('url', '')})")
                
                with col2:
                    st.write(f"**Relevance:** {article.get('relevance_score', 0):.2f}")
                    st.write(f"**Stance:** {article.get('stance', 'Unknown')}")

def display_fact_check(result):
    """Display fact-check results"""
    fact_check = result.get("fact_check_result")
    
    if fact_check:
        st.subheader("✅ Fact-Check Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Verdict:** {fact_check.get('verdict', 'Unknown')}")
            st.write(f"**Confidence:** {fact_check.get('confidence', 0):.1%}")
            st.write(f"**Source:** {fact_check.get('best_source', 'Unknown')}")
        
        with col2:
            st.write(f"**Review Date:** {fact_check.get('review_date', 'Unknown')}")
            st.write(f"**Explanation:** {fact_check.get('explanation', 'No explanation')}")
            
            if fact_check.get('url'):
                st.write(f"**URL:** [{fact_check.get('url', '')}]({fact_check.get('url', '')})")

def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown('<h1 class="main-header">🔍 TruthLens</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Fact-Checking System</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API URL configuration
        api_url = st.text_input(
            "API Base URL",
            value=API_BASE_URL,
            help="URL of your TruthLens API"
        )
        
        # Check API health
        if st.button("🔍 Check API Health"):
            if check_api_health():
                st.success("✅ API is running!")
            else:
                st.error("❌ API is not accessible")
        
        st.markdown("---")
        
        # Example claims
        st.header("💡 Example Claims")
        example_claims = [
            "The Eiffel Tower is in Paris",
            "The Earth is flat",
            "Vaccines cause autism",
            "Climate change is real",
            "The moon landing was fake",
            "5G causes coronavirus"
        ]
        
        for claim in example_claims:
            if st.button(claim, key=f"example_{claim}"):
                st.session_state.claim_input = claim
    
    # Main content
    if not check_api_health():
        st.error("""
        ⚠️ **API Connection Error**
        
        The TruthLens API is not accessible. Please ensure:
        1. The API is running on the specified URL
        2. The URL is correct in the sidebar
        3. The API is healthy and responding
        
        You can start the API locally with:
        ```bash
        python app_demo.py
        ```
        """)
        return
    
    # Claim input
    st.header("📝 Verify a Claim")
    
    # Get claim from session state or input
    default_claim = st.session_state.get("claim_input", "")
    
    claim = st.text_area(
        "Enter the claim you want to verify:",
        value=default_claim,
        height=100,
        placeholder="e.g., The Eiffel Tower is in Paris"
    )
    
    context = st.text_input(
        "Context (optional):",
        placeholder="e.g., Claim made on social media"
    )
    
    # Verify button
    if st.button("🔍 Verify Claim", type="primary"):
        if not claim.strip():
            st.warning("Please enter a claim to verify.")
        else:
            with st.spinner("🔍 Verifying claim..."):
                result = verify_claim(claim.strip(), context.strip())
            
            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                # Display results
                st.success("✅ Verification completed!")
                
                # Display verdict
                display_verdict(result)
                
                # Display metrics
                display_metrics(result)
                
                # Display stance analysis
                display_stance_analysis(result)
                
                # Display fact-check results
                display_fact_check(result)
                
                # Display articles
                display_articles(result)
                
                # Raw JSON (collapsible)
                with st.expander("📋 Raw API Response"):
                    st.json(result)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>🔍 TruthLens - AI-Powered Fact-Checking System</p>
        <p>Built with FastAPI, Streamlit, and advanced NLP</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
