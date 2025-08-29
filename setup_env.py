import subprocess
import sys
import logging
import pkg_resources

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_package(package_name: str) -> bool:
    """Check if a package is installed"""
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False

def setup_environment():
    """Install required dependencies"""
    requirements = [
        'aiohttp==3.8.1',
        'tenacity==8.0.1',
        'beautifulsoup4==4.9.3',
        'fastapi==0.68.0',
        'uvicorn==0.15.0',
        'requests>=2.26.0'
    ]
    
    print("\n=== Setting up TruthLens Environment ===")
    
    for req in requirements:
        package_name = req.split('==')[0]
        if not check_package(package_name):
            try:
                print(f"Installing {req}...")
                subprocess.check_call([
                    sys.executable, 
                    '-m', 
                    'pip', 
                    'install', 
                    '--disable-pip-version-check',
                    req
                ])
                if check_package(package_name):
                    print(f"✓ {package_name} installed successfully")
                else:
                    print(f"✗ Failed to verify {package_name} installation")
                    return False
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install {req}: {e}")
                return False
        else:
            print(f"✓ {package_name} already installed")
    
    print("\n✅ All dependencies installed!")
    return True

if __name__ == "__main__":
    if setup_environment():
        print("\nYou can now run: python test_scraper.py")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
