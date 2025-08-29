import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, Mock
from src.data_collection import fetch_url, collect_from_urls, RateLimiter
import pytest
import asyncio
from aiohttp import ClientSession

class TestDataCollection(unittest.TestCase):
    def setUp(self):
        self.test_url = "https://example.com"
        self.test_urls = [self.test_url, "https://example.org"]

    @patch('requests.get')
    def test_fetch_url(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>Test</html>"
        mock_get.return_value = mock_response

        result = fetch_url(self.test_url)
        self.assertEqual(result['status'], "200")  # Compare with string
        self.assertIn('html', result)
        self.assertIsNone(result['error'])

    @patch('src.data_collection.fetch_url')
    def test_collect_from_urls(self, mock_fetch):
        mock_fetch.return_value = {'status': 200, 'html': 'test'}
        results = collect_from_urls(self.test_urls)
        self.assertEqual(len(results), 2)

@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = RateLimiter(requests_per_second=2)
    domain = "example.com"
    
    start_time = time.time()
    await limiter.acquire(domain)
    await limiter.acquire(domain)
    elapsed = time.time() - start_time
    
    assert elapsed >= 0.5  # Should wait at least 500ms between requests

@pytest.mark.asyncio
async def test_fetch_url():
    async with ClientSession() as session:
        limiter = RateLimiter()
        result = await fetch_url(
            "https://example.com",
            session,
            limiter
        )
        assert result['status'] in [200, None]
        assert 'error' in result

@pytest.mark.asyncio
async def test_collect_from_urls():
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    results = await collect_from_urls(urls, concurrency=2)
    assert len(results) == len(urls)
    assert all('status' in r for r in results)

if __name__ == '__main__':
    unittest.main()
