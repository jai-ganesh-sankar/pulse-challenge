import re
from urllib.parse import urlparse, urljoin
from utils.logger import logger

def is_valid_url(url: str) -> bool:
    """
    Validates if a given string is a well-formed URL.
    """
    try:
        result = urlparse(url)
        # Check for scheme (http, https) and netloc (domain)
        # Also, a basic regex check to ensure it looks like a web URL
        if not all([result.scheme, result.netloc]):
            logger.warning(f"URL validation failed: Missing scheme or netloc for {url}")
            return False
        # A more robust regex might be needed for production, but this is a good start
        if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', url):
            logger.warning(f"URL validation failed: Regex mismatch for {url}")
            return False
        return True
    except ValueError as e:
        logger.error(f"URL parsing error for {url}: {e}")
        return False

def get_base_domain(url: str) -> str:
    """
    Extracts the base domain from a given URL.
    e.g., "https://help.instagram.com/articles/123" -> "help.instagram.com"
    """
    return urlparse(url).netloc

def normalize_url(base_url: str, relative_url: str) -> str:
    """
    Normalizes a relative URL against a base URL.
    """
    return urljoin(base_url, relative_url)

