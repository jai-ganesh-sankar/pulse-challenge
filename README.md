# Pulse AI Module Extractor

## Overview

This project implements an AI-powered Streamlit application that extracts structured information (key modules, submodules, and their detailed descriptions) from documentation-based help websites. It leverages a robust web crawler, an intelligent content preprocessor, and a powerful Large Language Model (LLM) using an efficient two-pass strategy for analysis and synthesis.

## Features

* **URL Input:** Accepts one documentation URLs.
* **Efficient Web Crawling:** Recursively crawls relevant pages using smart heuristics to stay on-topic and avoid irrelevant links.
* **Consolidated Content Preprocessing:** Cleans and aggregates content from all crawled pages into a single corpus for comprehensive analysis.
* **Two-Pass AI Extraction:**
  * **Pass 1 (Extraction):** Analyzes chunks of the consolidated text to perform a wide, raw extraction of all potential modules.
  * **Pass 2 (Synthesis):** Uses a single, final API call to merge, de-duplicate, and refine the raw data into a clean, logical, and accurate final structure.
* **Structured JSON Output:** Returns results in a standardized JSON format.
* **Minimalist User Interface:** A clean and simple web interface built with Streamlit.

## Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/pulse-ai-module-extractor.git](https://github.com/jai-ganesh-sankar/pulse-challenge.git)
    cd pulse-ai-module-extractor
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your OpenAI API Key:**

    * Create a `.env` file in the root directory.
    * Add your API key: `OPENAI_API_KEY="sk-xxxxxxxx"`

## Usage

1. **Run the Streamlit application:**

    ```bash
    streamlit run main.py
    ```

2. **Open your browser:** The application will open at `http://localhost:8501`.

3. **Enter URLs:** In the text area, enter one or more documentation URLs (one per line).

4. **Extract Modules:** Click the "Extract Modules" button to begin the process.

---

## Architecture and Design Rationale

The application is engineered for efficiency and quality using a multi-phase pipeline.

1. **Phase 1: Comprehensive Crawling**
    * The `WebCrawler` explores the site from a given URL. It uses a robust heuristic filter—not AI—to decide which links to follow. This approach is extremely fast and avoids wasting API calls on navigation. It effectively identifies relevant documentation pages while ignoring links to logins, marketing pages, or external sites.

2. **Phase 2: Content Consolidation & Preprocessing**
    * The content from all crawled pages is collected. The `ContentPreprocessor` strips away irrelevant HTML elements like navigation bars, footers, and scripts. It then extracts meaningful content (headings, paragraphs, lists) and combines it all into a single, clean text corpus. This ensures the AI has a comprehensive view of the entire documentation at once.

3. **Phase 3: Two-Pass AI Analysis**
    * This is the core of the system's intelligence, designed to maximize quality while minimizing cost.
    * **Pass 1 (Raw Extraction):** The `LLMModuleExtractor` chunks the consolidated text and sends each chunk to the LLM. The prompt asks the AI to find any and all potential modules and submodules within that chunk. This first pass is designed to be fast and broad, resulting in a "messy" but comprehensive collection of raw data.
    * **Pass 2 (Synthesis & Cleaning):** All the raw JSON data from Pass 1 is aggregated into a single file. This file is then sent back to the LLM in **one final API call**. The AI is given a different prompt, instructing it to act as a data analyst: merge duplicate modules, combine descriptions, de-duplicate submodules, and organize everything into a clean, final, and logically coherent JSON output.

This two-pass architecture is significantly more efficient and cost-effective than a naive page-by-page analysis, and it produces a more holistic and accurate final result.

---

## Known Limitations & Performance Considerations

1. **API Rate Limits and Cost**
    * This application relies on external LLM APIs (e.g., OpenAI), which are subject to rate limits and costs. The two-pass architecture was specifically designed to be efficient by drastically reducing the number of API calls compared to a page-by-page approach. However, processing exceptionally large websites on a restrictive plan (e.g., a free tier) may still trigger rate limit errors (`429 Too Many Requests`).

2. **Processing Time for Large Websites**
    * The overall processing time is directly proportional to the size of the target website—specifically, the number of pages crawled and the total amount of text. While the process is heavily optimized, users should expect longer wait times when analyzing very large documentation hubs.

3. **LLM Context Window for Synthesis**
    * The final synthesis pass requires that the entire collection of raw extracted modules fits within the LLM's context window. For the vast majority of websites, this is not an issue. However, for an exceptionally large site, this collection could theoretically exceed the token limit. In this scenario, the system is designed to gracefully fall back and will return the raw, un-synthesized data from Pass 1 instead of failing.

4. **Dynamic (JavaScript-Rendered) Content**
    * The current crawler uses `requests` and `BeautifulSoup`, which do not execute JavaScript. Websites that rely heavily on client-side JavaScript to load their content will not be fully crawled or processed. A headless browser solution (e.g., Selenium or Playwright) would be required to support these cases.

5. **Preprocessor Accuracy**
    * The `ContentPreprocessor` uses common semantic tags (`<main>`, `<article>`, etc.) to find the main documentation content. Websites with highly unusual or non-standard HTML structures may not be parsed optimally, which could affect the quality of the text provided to the LLM.

## Testing

Test results from running the application on several sample websites can be found in `testing.md`.
