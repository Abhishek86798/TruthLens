import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_nlp():
    """Install and set up NLP dependencies."""
    print("\n=== Setting up NLP Dependencies ===")
    
    # Required packages
    packages = [
        'nltk==3.8.1',
        'textstat==0.7.3'
    ]
    
    # Install packages
    for package in packages:
        print(f"\nInstalling {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")
            return False
    
    # Download NLTK data
    print("\nDownloading NLTK data...")
    try:
        import nltk
        nltk.download('vader_lexicon', quiet=True)
        print("✓ VADER lexicon downloaded successfully")
    except Exception as e:
        print(f"Failed to download NLTK data: {e}")
        return False
    
    print("\n✅ NLP setup completed successfully!")
    return True

if __name__ == "__main__":
    setup_nlp()
