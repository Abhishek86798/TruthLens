#!/usr/bin/env python3
"""
Simple test script for TruthLens Demo API
"""

import requests
import json
import time

def test_demo_api():
    """Test the demo API endpoints"""
    
    # Test claims
    test_claims = [
        "The Eiffel Tower is in Paris",
        "The Earth is flat",
        "Vaccines cause autism",
        "Climate change is real"
    ]
    
    base_url = "http://localhost:8000"
    
    print("🚀 TruthLens Demo API Test")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
        else:
            print("❌ Health check failed")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Message: {response.json()['message']}")
        else:
            print("❌ Root endpoint failed")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test components status
    try:
        response = requests.get(f"{base_url}/components-status", timeout=5)
        if response.status_code == 200:
            print("✅ Components status working")
            components = response.json()['components']
            print(f"   News API: {components['news_api']}")
            print(f"   Guardian API: {components['guardian_api']}")
            print(f"   Google FactCheck: {components['google_factcheck']}")
        else:
            print("❌ Components status failed")
    except Exception as e:
        print(f"❌ Components status error: {e}")
    
    print("\n🔍 Testing claim verification:")
    
    for claim in test_claims:
        print(f"\n📝 Testing: '{claim}'")
        try:
            payload = {
                "claim": claim,
                "context": "Demo test"
            }
            
            response = requests.post(
                f"{base_url}/verify",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Verdict: {result.get('verdict', 'Unknown')}")
                print(f"   Confidence: {result.get('confidence', 0):.1%}")
                print(f"   Articles Found: {result.get('total_articles', 0)}")
                print(f"   Processing Time: {result.get('processing_time', 0):.2f}s")
                
                # Show stance distribution
                stance_dist = result.get('stance_distribution', {})
                if stance_dist:
                    print(f"   Stance: Support={stance_dist.get('support', 0)}, "
                          f"Contradict={stance_dist.get('contradict', 0)}, "
                          f"Neutral={stance_dist.get('neutral', 0)}")
                
                # Show fact-check result if available
                fact_check = result.get('fact_check_result')
                if fact_check:
                    print(f"   Fact-Check: {fact_check.get('verdict', 'Unknown')}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    print("\n🎉 Demo API test completed!")

if __name__ == "__main__":
    test_demo_api()
