import os

def generate_github_workflow():
    workflow = '''# filepath: c:\TruthLens\.github\workflows\python-app.yml
name: TruthLens CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test with pytest
      run: |
        pytest tests/ --cov=src --cov-report=term-missing
'''
    
    print("\n=== GitHub Actions Workflow for TruthLens ===")
    print("This workflow will:")
    print("1. Run on push/PR to main branch")
    print("2. Test against Python 3.9, 3.10, and 3.11")
    print("3. Install dependencies")
    print("4. Run flake8 linting")
    print("5. Run pytest with coverage")
    print("\nWorkflow YAML contents:")
    print("-" * 50)
    print(workflow)
    print("-" * 50)
    print("\nTo use:")
    print("1. Create .github/workflows directory")
    print("2. Save as 'python-app.yml' in that directory")

if __name__ == "__main__":
    try:
        generate_github_workflow()
    finally:
        print("\nCleaning up test file...")
        os.remove(__file__)
