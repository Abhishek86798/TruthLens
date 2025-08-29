from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Data Collection
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    REQUEST_TIMEOUT: int = 30
    
    # Rate Limiting
    RATE_LIMIT: int = 100
    RATE_WINDOW: int = 60
    
    # Processing
    MIN_CONTENT_LENGTH: int = 50
    DEDUP_THRESHOLD: float = 0.85
    
    # Model
    MODEL_VERSION: str = "0.1.0"
    FEATURE_FLAGS: dict = {
        "use_async": True,
        "use_cache": True,
        "use_dedup": True
    }

class DataCollectionSettings(BaseSettings):
    CONCURRENCY_LIMIT: int = 5
    REQUESTS_PER_SECOND: float = 2.0
    MAX_RETRIES: int = 3
    RETRY_MIN_DELAY: int = 4
    RETRY_MAX_DELAY: int = 30
    REQUEST_TIMEOUT: int = 30
    
    class Config:
        env_prefix = "TRUTHLENS_"

settings = Settings()
data_collection_settings = DataCollectionSettings()
