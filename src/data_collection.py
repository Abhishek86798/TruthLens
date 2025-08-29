import aiohttp
import asyncio
import random
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
import logging
from aiohttp import ClientSession
from tenacity import retry, wait_exponential, stop_after_attempt

logger = logging.getLogger(__name__)

# Constants
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

class RateLimiter:
    def __init__(self, requests_per_second: float = 2.0):
        self.rate = requests_per_second
        self.last_request = {}
        self._lock = asyncio.Lock()
    
    async def acquire(self, domain: str):
        async with self._lock:
            now = time.time()
            if domain in self.last_request:
                elapsed = now - self.last_request[domain]
                if elapsed < 1.0/self.rate:
                    await asyncio.sleep(1.0/self.rate - elapsed)
            self.last_request[domain] = time.time()

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=30),
    stop=stop_after_attempt(3)
)
async def fetch_url(
    url: str,
    session: ClientSession,
    rate_limiter: RateLimiter,
    proxy: Optional[str] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Fetch URL with retry logic and rate limiting."""
    domain = urlparse(url).netloc
    await rate_limiter.acquire(domain)
    
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    
    try:
        async with session.get(
            url,
            headers=headers,
            proxy=proxy,
            timeout=timeout
        ) as response:
            return {
                'url': url,
                'status': response.status,
                'html': await response.text(),
                'error': None
            }
    except Exception as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        return {
            'url': url,
            'status': None,
            'html': None,
            'error': str(e)
        }

async def collect_from_urls(
    urls: List[str],
    concurrency: int = 5,
    proxy_list: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """Collect content from multiple URLs concurrently."""
    rate_limiter = RateLimiter()
    results = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            proxy = random.choice(proxy_list) if proxy_list else None
            task = asyncio.create_task(
                fetch_url(url, session, rate_limiter, proxy)
            )
            tasks.append(task)
            
            if len(tasks) >= concurrency:
                completed = await asyncio.gather(*tasks)
                results.extend(completed)
                tasks = []
        
        if tasks:
            completed = await asyncio.gather(*tasks)
            results.extend(completed)
    
    return results

def fetch_url_sync(url: str, timeout: int = 15) -> Dict[str, Optional[str]]:
    """Fetch content from a single URL (synchronously)."""
    try:
        response = requests.get(url, timeout=timeout)
        return {
            'url': url,
            'status': str(response.status_code),
            'html': response.text,
            'error': None
        }
    except Exception as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        return {
            'url': url,
            'status': None,
            'html': None,
            'error': str(e)
        }

def collect_from_urls_sync(urls: List[str], timeout: int = 15) -> List[Dict[str, Optional[str]]]:
    """Collect content from multiple URLs (synchronously)."""
    return [fetch_url_sync(url, timeout) for url in urls]
