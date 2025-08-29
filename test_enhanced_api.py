#!/usr/bin/env python3
"""
Quick test for the enhanced TruthLens API
"""

import requests
import json

def test_enhanced_api():
    """Test the enhanced API"""
    
    print("🔍 Testing Enhanced TruthLens API")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:8001/health", timeout=10)
        if response.status_code == 200:
            print("✅ Enhanced API is running on port 8001")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to enhanced API: {e}")
        return
    
    # Test claim verification
    test_claims = [
        "5G causes coronavirus",
        "The Earth is flat", 
        "Vaccines cause autism",
        "Climate change is real"
    ]
    
    for claim in test_claims:
        print(f"\n🔍 Testing: '{claim}'")
        
        try:
            payload = {
                "claim": claim,
                "context": "API test"
            }
            
            response = requests.post(
                "http://localhost:8001/verify",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Verdict: {result['verdict']}")
                print(f"   Confidence: {result['confidence']:.1%}")
                print(f"   Articles: {result['total_articles']}")
                print(f"   Time: {result['processing_time']:.2f}s")
                
                if result['fact_check_result']:
                    fact_check = result['fact_check_result']
                    print(f"   Fact Check: {fact_check.get('verdict', 'Unknown')}")
            else:
                print(f"❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Enhanced API test completed!")

if __name__ == "__main__":
    test_enhanced_api()
