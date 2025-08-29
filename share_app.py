#!/usr/bin/env python3
"""
Script to share TruthLens Streamlit app publicly using ngrok
"""

from pyngrok import ngrok
import subprocess
import time
import sys
import os

def share_streamlit_app():
    """Share the Streamlit app publicly"""
    
    print("🔍 TruthLens App Sharing")
    print("=" * 40)
    
    # Check if Streamlit is running
    try:
        import requests
        response = requests.get("http://localhost:8502", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit app is running on localhost:8502")
        else:
            print("❌ Streamlit app is not accessible")
            return
    except:
        print("❌ Streamlit app is not running")
        print("Please start it first with: streamlit run streamlit_demo.py")
        return
    
    # Create ngrok tunnel
    print("\n🌐 Creating public tunnel...")
    try:
        # Create HTTP tunnel to Streamlit
        public_url = ngrok.connect(8502)
        print(f"✅ Public URL created: {public_url}")
        
        print("\n🎉 Your TruthLens app is now publicly accessible!")
        print(f"📱 Share this URL with anyone: {public_url}")
        print("\n💡 Features available:")
        print("   - Claim verification")
        print("   - Article analysis")
        print("   - Stance detection")
        print("   - Fact-check results")
        
        print("\n⚠️  Important notes:")
        print("   - This URL will work as long as this script is running")
        print("   - Close this script to stop the public access")
        print("   - For permanent hosting, use Streamlit Cloud")
        
        print("\n🔄 Keeping tunnel active... (Press Ctrl+C to stop)")
        
        # Keep the tunnel alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping public access...")
            ngrok.kill()
            print("✅ Public access stopped")
            
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        print("Make sure you have ngrok installed and configured")

if __name__ == "__main__":
    share_streamlit_app()
