import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse, urljoin
from utils.logger import logger
from utils.url_validators import get_base_domain, is_valid_url

class WebCrawler:
    """
    A web crawler to fetch HTML content from documentation websites.
    It performs a Breadth-First Search (BFS) within the same domain
    and uses robust heuristic-based filtering to stay on topic.
    """
    def __init__(self, max_depth: int = 2, timeout: int = 10):
        """
        Initializes the WebCrawler.

        Args:
            max_depth (int): The maximum depth to crawl from the initial URL.
            timeout (int): Timeout for HTTP requests in seconds.
        """
        self.max_depth = max_depth
        self.timeout = timeout
        self.visited_urls = set()
        self.queue = deque()
        self.crawled_content = {} # Stores {url: html_content} for relevant pages

    def crawl(self, start_url: str) -> dict:
        """
        Starts the crawling process from a given URL.

        Args:
            start_url (str): The initial URL to start crawling from.

        Returns:
            dict: A dictionary where keys are crawled URLs and values are their HTML content.
        """
        if not is_valid_url(start_url):
            logger.error(f"Invalid starting URL provided: {start_url}")
            return {}

        base_domain = get_base_domain(start_url)
        if not base_domain:
            logger.error(f"Could not extract base domain from {start_url}")
            return {}

        self.queue.append((start_url, 0)) # (url, depth)
        self.visited_urls.add(start_url)
        logger.info(f"Starting crawl from: {start_url} (Base Domain: {base_domain})")

        while self.queue:
            current_url, depth = self.queue.popleft()

            if depth > self.max_depth:
                logger.debug(f"Skipping {current_url}: Max depth ({self.max_depth}) reached.")
                continue

            logger.info(f"Crawling (Depth {depth}): {current_url}")
            html_content = self._fetch_page(current_url)

            if html_content:
                self.crawled_content[current_url] = html_content
                
                raw_links_info = self._extract_links_info(html_content, current_url)

                # Use the new, fast heuristic filter instead of slow AI calls
                links_to_add = [
                    link_info['url'] for link_info in raw_links_info
                    if self._is_relevant_link(link_info['url'], link_info['anchor_text'])
                ]
                logger.info(f"Using heuristic filtering. Found {len(links_to_add)} relevant links out of {len(raw_links_info)} total.")


                for link in links_to_add:
                    link_domain = get_base_domain(link)
                    if link_domain == base_domain and link not in self.visited_urls:
                        self.queue.append((link, depth + 1))
                        self.visited_urls.add(link)
                        logger.debug(f"Added to queue: {link} (Depth {depth + 1})")
                    else:
                        logger.debug(f"Skipping external or already visited link: {link}")
            else:
                logger.warning(f"No content fetched for {current_url}")

        logger.info(f"Crawling finished. Found {len(self.crawled_content)} relevant pages.")
        return self.crawled_content

    def _fetch_page(self, url: str) -> str | None:
        """
        Fetches the HTML content of a given URL.

        Args:
            url (str): The URL to fetch.

        Returns:
            str | None: The HTML content as a string, or None if an error occurred.
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, timeout=self.timeout, allow_redirects=True, headers=headers)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def _is_relevant_link(self, url: str, anchor_text: str) -> bool:
        """
        A robust heuristic filter to determine if a link is likely to be a documentation page.
        """
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        lower_anchor = anchor_text.lower()

        # 1. Exclude mailto, tel, and javascript links
        if parsed_url.scheme not in ['http', 'https']:
            return False

        # 2. Exclude based on file extensions for non-HTML content
        excluded_extensions = [
            '.pdf', '.zip', '.exe', '.dmg', '.pkg', '.msi',
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
            '.css', '.js', '.xml', '.rss', '.json', '.sh', '.py'
        ]
        if any(path.endswith(ext) for ext in excluded_extensions):
            return False

        # 3. Exclude common non-documentation paths
        excluded_paths = [
            '/blog', '/news', '/about', '/contact', '/careers', '/jobs',
            '/login', '/signup', '/signin', '/register', '/account', '/profile',
            '/privacy', '/terms', '/legal', '/policy', '/security',
            '/pricing', '/demo', '/webinar', '/events', '/case-studies',
            '/community', '/forum', '/company', '/press', '/brand', '/investors'
        ]
        if any(p in path for p in excluded_paths):
            return False

        # 4. Exclude based on anchor text clues for non-documentation links
        excluded_anchors = [
            'log in', 'sign in', 'sign up', 'register', 'contact us', 'about us',
            'privacy policy', 'terms of service', 'careers', 'pricing', 'request a demo',
            'download', 'follow us', 'facebook', 'twitter', 'linkedin', 'youtube'
        ]
        if any(anchor in lower_anchor for anchor in excluded_anchors):
            return False

        # If it hasn't been excluded by any rule, assume it's relevant.
        return True

    def _extract_links_info(self, html_content: str, base_url: str) -> list[dict]:
        """
        Extracts all absolute links and their anchor text from the HTML content.

        Args:
            html_content (str): The HTML content to parse.
            base_url (str): The base URL to resolve relative links.

        Returns:
            list[dict]: A list of dictionaries, each with 'url' and 'anchor_text'.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links_info = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            # Basic check to ensure it's an http/https link and not just a fragment
            if full_url.startswith(('http://', 'https://')):
                anchor_text = a_tag.get_text(strip=True)
                links_info.append({'url': full_url, 'anchor_text': anchor_text})
        return links_info