from bs4 import BeautifulSoup, Tag
from utils.logger import logger

class ContentPreprocessor:
    """
    Cleans and preprocesses HTML content to extract meaningful text
    and represent it in a structured format suitable for LLM input.
    """
    def __init__(self):
        pass

    def clean_html(self, html_content: str) -> BeautifulSoup | None:
        """
        Parses HTML and removes irrelevant elements like headers, footers,
        navigation, scripts, styles, etc., to isolate the main content.

        Args:
            html_content (str): The raw HTML content of a page.

        Returns:
            BeautifulSoup | None: A BeautifulSoup object containing the cleaned HTML,
                                  or None if parsing fails.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove common irrelevant tags and their content
            irrelevant_tags = [
                'script', 'style', 'noscript', 'head', 'footer', 'nav', 'aside',
                'form', 'iframe', 'img', 'svg', 'button', 'input', 'select', 'textarea'
            ]
            for tag_name in irrelevant_tags:
                for tag in soup.find_all(tag_name):
                    tag.decompose()

            # Remove elements by common class/id names that indicate non-content sections
            irrelevant_classes_ids = [
                'header', 'footer', 'navbar', 'navigation', 'sidebar', 'ads',
                'related-articles', 'comments', 'feedback', 'breadcrumb',
                'skip-link', 'sr-only', 'visually-hidden', # Accessibility helpers often contain hidden text
                'toc', # Table of contents - we want to infer structure, not just copy it
                'meta', 'social-share', 'print-button'
            ]
            for class_id in irrelevant_classes_ids:
                for tag in soup.find_all(class_=class_id):
                    tag.decompose()
                for tag in soup.find_all(id=class_id):
                    tag.decompose()

            # Attempt to find the main content area more intelligently
            # Prioritize semantic tags or common content IDs/classes
            main_content_candidates = soup.find_all(['main', 'article', 'div'],
                                                     class_=['main-content', 'article-body', 'content', 'post-content', 'documentation-content'])
            if main_content_candidates:
                # Take the largest candidate, or the first good one
                main_content_soup = max(main_content_candidates, key=lambda tag: len(tag.get_text(strip=True)), default=soup)
                logger.debug(f"Identified main content area based on tag/class.")
            else:
                # Fallback: Use the body or the entire soup if no specific main content found
                main_content_soup = soup.find('body') or soup
                logger.warning("No specific main content area identified, using body or entire soup as fallback.")

            return main_content_soup
        except Exception as e:
            logger.error(f"Error cleaning HTML: {e}")
            return None

    def extract_structured_text(self, cleaned_soup: BeautifulSoup) -> list[str]:
        """
        Extracts text content from the cleaned HTML, preserving hierarchy
        by marking headings. This prepares the text for LLM input.

        Args:
            cleaned_soup (BeautifulSoup): The BeautifulSoup object with cleaned HTML.

        Returns:
            list[str]: A list of strings, where each string is a paragraph,
                       list item, or a heading (prefixed with Markdown-like ##).
        """
        structured_content = []
        if not cleaned_soup:
            return structured_content

        # Iterate through common block-level elements that indicate content flow
        for element in cleaned_soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'div', 'section', 'article', 'ul', 'ol', 'table']):
            text = element.get_text(strip=True)
            if not text:
                continue

            if element.name.startswith('h'):
                level = int(element.name[1])
                # Use Markdown-like headings for LLM input
                structured_content.append(f"{'#' * level} {text}")
            elif element.name == 'p':
                structured_content.append(text)
            elif element.name == 'li':
                # Prepend a bullet for list items
                structured_content.append(f"- {text}")
            elif element.name in ['ul', 'ol']:
                # For ul/ol, we already process li children, so skip the parent if empty
                pass
            elif element.name == 'table':
                # Basic table processing: extract header and rows
                table_text = []
                headers = [th.get_text(strip=True) for th in element.find_all('th')]
                if headers:
                    table_text.append("| " + " | ".join(headers) + " |")
                    table_text.append("|" + "---|"*len(headers))
                for row in element.find_all('tr'):
                    cells = [td.get_text(strip=True) for td in row.find_all('td')]
                    if cells:
                        table_text.append("| " + " | ".join(cells) + " |")
                if table_text:
                    structured_content.append("\n".join(table_text))
            elif element.name in ['div', 'section', 'article']:
                # For generic divs/sections, only add their text if they don't contain
                # other structured elements that would be processed separately.
                # This prevents duplicate content.
                # A more sophisticated check might be needed here.
                if not any(child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'ul', 'ol', 'table'] for child in element.children):
                    structured_content.append(text)

        # Filter out empty strings or strings that are just whitespace
        structured_content = [s for s in structured_content if s.strip()]

        logger.info(f"Extracted {len(structured_content)} structured text blocks.")
        return structured_content

