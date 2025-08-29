#!/usr/bin/env python3
"""
TruthLens Demo Launcher
Choose between different demo interfaces
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'gradio', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install streamlit gradio requests")
        return False
    
    return True

def check_api_running():
    """Check if the API is running"""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_api():
    """Start the API server"""
    print("🚀 Starting TruthLens API...")
    try:
        # Start API in background
        api_process = subprocess.Popen([
            sys.executable, "app_demo.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for API to start
        time.sleep(3)
        
        if api_process.poll() is None:
            print("✅ API started successfully!")
            return api_process
        else:
            print("❌ Failed to start API")
            return None
            
    except Exception as e:
        print(f"❌ Error starting API: {e}")
        return None

def main():
    """Main launcher function"""
    print("🔍 TruthLens Demo Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check if API is running
    api_running = check_api_running()
    api_process = None
    
    if not api_running:
        print("⚠️  API not running. Starting it now...")
        api_process = start_api()
        if not api_process:
            print("❌ Cannot start API. Please start it manually with: python app_demo.py")
            return
    else:
        print("✅ API is already running!")
    
    print("\n🎯 Choose your demo interface:")
    print("1. Streamlit (Recommended - Beautiful UI)")
    print("2. Gradio (Alternative - Shareable URL)")
    print("3. API Only (Command line testing)")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting Streamlit demo...")
            print("📱 Streamlit will open in your browser at: http://localhost:8501")
            print("💡 Press Ctrl+C to stop")
            
            try:
                subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_demo.py"])
            except KeyboardInterrupt:
                print("\n⏹️  Streamlit stopped")
            except Exception as e:
                print(f"❌ Error starting Streamlit: {e}")
        
        elif choice == "2":
            print("\n🚀 Starting Gradio demo...")
            print("📱 Gradio will open in your browser at: http://localhost:7860")
            print("🌐 A temporary public URL will be generated for sharing")
            print("💡 Press Ctrl+C to stop")
            
            try:
                subprocess.run([sys.executable, "gradio_demo.py"])
            except KeyboardInterrupt:
                print("\n⏹️  Gradio stopped")
            except Exception as e:
                print(f"❌ Error starting Gradio: {e}")
        
        elif choice == "3":
            print("\n🔧 API Testing Mode")
            print("📡 API is running at: http://localhost:8000")
            print("📖 API Documentation: http://localhost:8000/docs")
            print("💡 Use test_demo.py to test the API")
            
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    
    # Clean up API process if we started it
    if api_process:
        print("\n🛑 Stopping API...")
        api_process.terminate()
        api_process.wait()
        print("✅ API stopped")

if __name__ == "__main__":
    main()
