from setuptools import setup, find_packages

setup(
    name="truthlens",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'requests>=2.26.0',
        'langdetect>=1.0.9',
        'readability-lxml>=0.8.1',
        'aiohttp>=3.8.1',
        'pandas>=1.3.0'
    ]
)
