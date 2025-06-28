import streamlit as st
import os
from dotenv import load_dotenv

from utils.logger import logger
from utils.url_validators import is_valid_url
from core.crawler import WebCrawler
from core.preprocessor import ContentPreprocessor
from core.ai_extractor import LLMModuleExtractor

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Streamlit UI ---
st.set_page_config(page_title="Pulse AI Module Extractor", layout="wide")

st.title("Pulse AI Module Extractor")

st.markdown(
    """
    This application extracts structured information from documentation-based help websites.
    It identifies key modules and submodules, generating detailed descriptions for each based
    on the content from the URLs provided.
    """
)

# Input for URLs
url_input = st.text_area(
    "Enter one documentation URL:",
    height=150,
    placeholder="e.g.,\nhttps://support.spotify.com/in-en/"
)

# All sidebar elements have been removed from the code.

if st.button("Extract Modules"):
    if not url_input:
        st.error("Please enter at least one URL.")
    elif not OPENAI_API_KEY:
        st.error("OpenAI API key not found. Please set the OPENAI_API_KEY in your .env file.")
    else:
        urls = [u.strip() for u in url_input.split('\n') if u.strip()]
        valid_urls = [url for url in urls if is_valid_url(url)]
        invalid_urls = [url for url in urls if not is_valid_url(url)]

        if invalid_urls:
            st.warning(f"Skipping invalid URLs: {', '.join(invalid_urls)}")

        if not valid_urls:
            st.error("No valid URLs provided after validation.")
        else:
            # Initialize components with hardcoded settings
            try:
                llm_extractor = LLMModuleExtractor(api_key=OPENAI_API_KEY, model_name="gpt-4o")
                crawler = WebCrawler(max_depth=1, timeout=15)
                preprocessor = ContentPreprocessor()
            except ValueError as e:
                st.error(f"Initialization error: {e}")
                st.stop()

            all_extracted_modules = []
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, url in enumerate(valid_urls):
                progress_bar.progress((i + 1) / len(valid_urls))

                try:
                    # Step 1: Crawl the entire site first
                    status_text.text(f"[{i+1}/{len(valid_urls)}] Step 1/3: Crawling site from {url}...")
                    crawled_html_content = crawler.crawl(url)
                    if not crawled_html_content:
                        st.warning(f"Could not crawl any content from {url}. Skipping.")
                        continue

                    # Step 2: Preprocess and consolidate all text
                    status_text.text(f"[{i+1}/{len(valid_urls)}] Step 2/3: Preprocessing {len(crawled_html_content)} pages...")
                    all_text_blocks = []
                    for crawled_url, html_content in crawled_html_content.items():
                        cleaned_soup = preprocessor.clean_html(html_content)
                        if cleaned_soup:
                            all_text_blocks.extend(preprocessor.extract_structured_text(cleaned_soup))

                    if not all_text_blocks:
                        st.warning(f"No text could be extracted after preprocessing {url}. Skipping.")
                        continue
                    
                    consolidated_text = "\n\n".join(all_text_blocks)
                    logger.info(f"Consolidated text for {url} contains {len(consolidated_text)} characters.")

                    # Step 3: Use the two-pass AI extractor
                    status_text.text(f"[{i+1}/{len(valid_urls)}] Step 3/3: AI is analyzing documentation...")
                    with st.spinner("AI is analyzing the entire documentation. This may take a moment..."):
                        extracted_data = llm_extractor.extract(consolidated_text)
                        if extracted_data:
                            all_extracted_modules.extend(extracted_data)

                except Exception as e:
                    st.error(f"A critical error occurred while processing {url}: {e}")
                    logger.error(f"Critical error processing {url}: {e}", exc_info=True)

            progress_bar.empty()
            status_text.empty()

            if all_extracted_modules:
                st.success("Module extraction complete!")
                st.subheader("Final Extracted Modules (JSON Output):")
                st.json(all_extracted_modules)
            else:
                st.warning("No modules or submodules could be extracted from the provided URLs.")