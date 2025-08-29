import os

def generate_dockerfile():
    dockerfile = '''# filepath: c:\TruthLens\Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE ${PORT}

# Start the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
'''
    
    print("\n=== Dockerfile Template for TruthLens API ===")
    print("This Dockerfile will:")
    print("1. Use Python 3.11 slim base image")
    print("2. Set up proper environment variables")
    print("3. Install system and Python dependencies")
    print("4. Configure uvicorn server")
    print("\nDockerfile contents:")
    print("-" * 50)
    print(dockerfile)
    print("-" * 50)
    print("\nTo use:")
    print("1. Save this as 'Dockerfile' in project root")
    print("2. Create requirements.txt")
    print("3. Run: docker build -t truthlens .")
    print("4. Run: docker run -p 8000:8000 truthlens")

if __name__ == "__main__":
    try:
        generate_dockerfile()
    finally:
        print("\nCleaning up test file...")
        os.remove(__file__)
