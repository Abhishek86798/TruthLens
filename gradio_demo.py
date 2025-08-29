#!/usr/bin/env python3
"""
TruthLens Gradio Demo Interface
A user-friendly web interface for fact-checking claims
"""

import gradio as gr
import requests
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
            "context": context or "Gradio demo verification"
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

def format_verdict_html(result):
    """Format verdict as HTML"""
    verdict = result.get("verdict", "Unknown")
    confidence = result.get("confidence", 0)
    reasoning = result.get("reasoning", "No reasoning provided")
    
    # Color coding based on verdict
    if "true" in verdict.lower():
        color = "#d4edda"
        text_color = "#155724"
    elif "false" in verdict.lower():
        color = "#f8d7da"
        text_color = "#721c24"
    else:
        color = "#fff3cd"
        text_color = "#856404"
    
    return f"""
    <div style="background-color: {color}; color: {text_color}; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h2>🔍 Verdict: {verdict}</h2>
        <p><strong>Confidence:</strong> {confidence:.1%}</p>
        <p><strong>Reasoning:</strong> {reasoning}</p>
    </div>
    """

def format_metrics_html(result):
    """Format metrics as HTML"""
    total_articles = result.get("total_articles", 0)
    processing_time = result.get("processing_time", 0)
    evidence_strength = result.get("evidence_strength", "Unknown")
    sources_count = len(result.get("sources_checked", []))
    
    return f"""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0;">
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #1f77b4;">
            <h3>📰 Articles Found</h3>
            <p style="font-size: 24px; font-weight: bold; color: #1f77b4;">{total_articles}</p>
        </div>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #1f77b4;">
            <h3>⏱️ Processing Time</h3>
            <p style="font-size: 24px; font-weight: bold; color: #1f77b4;">{processing_time:.2f}s</p>
        </div>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #1f77b4;">
            <h3>💪 Evidence Strength</h3>
            <p style="font-size: 24px; font-weight: bold; color: #1f77b4;">{evidence_strength}</p>
        </div>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #1f77b4;">
            <h3>🔗 Sources Used</h3>
            <p style="font-size: 24px; font-weight: bold; color: #1f77b4;">{sources_count}</p>
        </div>
    </div>
    """

def format_stance_analysis_html(result):
    """Format stance analysis as HTML"""
    stance_dist = result.get("stance_distribution", {})
    stance_pct = result.get("stance_percentages", {})
    
    if not stance_dist:
        return ""
    
    support = stance_dist.get("support", 0)
    contradict = stance_dist.get("contradict", 0)
    neutral = stance_dist.get("neutral", 0)
    
    support_pct = stance_pct.get("support", 0)
    contradict_pct = stance_pct.get("contradict", 0)
    neutral_pct = stance_pct.get("neutral", 0)
    
    return f"""
    <div style="margin: 20px 0;">
        <h3>📊 Stance Analysis</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
            <div style="background-color: #d4edda; padding: 15px; border-radius: 8px; text-align: center;">
                <h4>✅ Supporting</h4>
                <p style="font-size: 20px; font-weight: bold;">{support}</p>
                <p style="font-size: 14px;">{support_pct:.1%}</p>
            </div>
            <div style="background-color: #f8d7da; padding: 15px; border-radius: 8px; text-align: center;">
                <h4>❌ Contradicting</h4>
                <p style="font-size: 20px; font-weight: bold;">{contradict}</p>
                <p style="font-size: 14px;">{contradict_pct:.1%}</p>
            </div>
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; text-align: center;">
                <h4>🤷 Neutral</h4>
                <p style="font-size: 20px; font-weight: bold;">{neutral}</p>
                <p style="font-size: 14px;">{neutral_pct:.1%}</p>
            </div>
        </div>
    </div>
    """

def format_articles_html(result):
    """Format articles as HTML"""
    details = result.get("details", [])
    
    if not details:
        return ""
    
    articles_html = "<h3>📰 Related Articles</h3>"
    
    for i, article in enumerate(details[:5]):  # Show first 5 articles
        title = article.get("title", "No title")
        source = article.get("source", "Unknown")
        published = article.get("published_at", "Unknown")
        url = article.get("url", "")
        relevance = article.get("relevance_score", 0)
        stance = article.get("stance", "Unknown")
        
        articles_html += f"""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #e9ecef; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h4>Article {i+1}: {title[:50]}{'...' if len(title) > 50 else ''}</h4>
            <p><strong>Source:</strong> {source}</p>
            <p><strong>Published:</strong> {published}</p>
            <p><strong>Relevance:</strong> {relevance:.2f}</p>
            <p><strong>Stance:</strong> {stance}</p>
            {f'<p><strong>URL:</strong> <a href="{url}" target="_blank">{url}</a></p>' if url else ''}
        </div>
        """
    
    return articles_html

def format_fact_check_html(result):
    """Format fact-check results as HTML"""
    fact_check = result.get("fact_check_result")
    
    if not fact_check:
        return ""
    
    verdict = fact_check.get("verdict", "Unknown")
    confidence = fact_check.get("confidence", 0)
    source = fact_check.get("best_source", "Unknown")
    review_date = fact_check.get("review_date", "Unknown")
    explanation = fact_check.get("explanation", "No explanation")
    url = fact_check.get("url", "")
    
    return f"""
    <div style="background-color: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3>✅ Fact-Check Results</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p><strong>Verdict:</strong> {verdict}</p>
                <p><strong>Confidence:</strong> {confidence:.1%}</p>
                <p><strong>Source:</strong> {source}</p>
            </div>
            <div>
                <p><strong>Review Date:</strong> {review_date}</p>
                <p><strong>Explanation:</strong> {explanation}</p>
                {f'<p><strong>URL:</strong> <a href="{url}" target="_blank">{url}</a></p>' if url else ''}
            </div>
        </div>
    </div>
    """

def process_claim(claim, context):
    """Process claim verification and return formatted results"""
    if not claim.strip():
        return "Please enter a claim to verify.", ""
    
    # Check API health first
    if not check_api_health():
        return "❌ API Connection Error: The TruthLens API is not accessible. Please ensure the API is running.", ""
    
    # Verify claim
    result = verify_claim(claim.strip(), context.strip())
    
    if "error" in result:
        return f"❌ {result['error']}", ""
    
    # Format results as HTML
    html_output = f"""
    <div style="font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto;">
        <h1 style="text-align: center; color: #1f77b4; margin-bottom: 30px;">🔍 TruthLens - Fact Check Results</h1>
        
        {format_verdict_html(result)}
        {format_metrics_html(result)}
        {format_stance_analysis_html(result)}
        {format_fact_check_html(result)}
        {format_articles_html(result)}
        
        <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
            <h3>📋 Raw API Response</h3>
            <pre style="background-color: #ffffff; padding: 10px; border-radius: 5px; overflow-x: auto;">{json.dumps(result, indent=2)}</pre>
        </div>
    </div>
    """
    
    return "✅ Verification completed successfully!", html_output

def create_demo():
    """Create the Gradio interface"""
    
    # Custom CSS
    css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 20px;
    }
    """
    
    with gr.Blocks(css=css, title="TruthLens - AI Fact Checker") as demo:
        gr.HTML("""
        <div class="main-header">
            <h1>🔍 TruthLens</h1>
            <p style="font-size: 1.2rem; color: #666;">AI-Powered Fact-Checking System</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                claim_input = gr.Textbox(
                    label="📝 Enter the claim you want to verify",
                    placeholder="e.g., The Eiffel Tower is in Paris",
                    lines=3
                )
                
                context_input = gr.Textbox(
                    label="Context (optional)",
                    placeholder="e.g., Claim made on social media"
                )
                
                verify_btn = gr.Button("🔍 Verify Claim", variant="primary")
            
            with gr.Column(scale=1):
                gr.HTML("""
                <h3>💡 Example Claims</h3>
                <ul>
                    <li>The Eiffel Tower is in Paris</li>
                    <li>The Earth is flat</li>
                    <li>Vaccines cause autism</li>
                    <li>Climate change is real</li>
                    <li>The moon landing was fake</li>
                    <li>5G causes coronavirus</li>
                </ul>
                """)
        
        # Status output
        status_output = gr.Textbox(
            label="Status",
            interactive=False
        )
        
        # Results output
        results_output = gr.HTML(
            label="Results"
        )
        
        # Connect button to function
        verify_btn.click(
            fn=process_claim,
            inputs=[claim_input, context_input],
            outputs=[status_output, results_output]
        )
        
        # Example buttons
        examples = [
            ["The Eiffel Tower is in Paris", "Tourist information"],
            ["The Earth is flat", "Social media claim"],
            ["Vaccines cause autism", "Health misinformation"],
            ["Climate change is real", "Scientific consensus"],
            ["The moon landing was fake", "Conspiracy theory"],
            ["5G causes coronavirus", "Technology misinformation"]
        ]
        
        gr.Examples(
            examples=examples,
            inputs=[claim_input, context_input],
            label="💡 Try these examples"
        )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; color: #666; font-size: 0.8rem; margin-top: 30px; padding: 20px; border-top: 1px solid #e9ecef;">
            <p>🔍 TruthLens - AI-Powered Fact-Checking System</p>
            <p>Built with FastAPI, Gradio, and advanced NLP</p>
        </div>
        """)
    
    return demo

if __name__ == "__main__":
    # Create and launch the demo
    demo = create_demo()
    
    # Launch with sharing enabled for temporary public URL
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,  # This creates a temporary public URL
        show_error=True
    )
