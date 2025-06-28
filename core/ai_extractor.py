import openai
import json
import tiktoken
from utils.logger import logger

class LLMModuleExtractor:
    """
    Handles interaction with the LLM for extracting modules using an efficient
    two-pass (extract and synthesize) approach.
    """
    def __init__(self, api_key: str, model_name: str = "gpt-4o"):
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        self.api_key = api_key
        self.model_name = model_name
        # self.client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=self.api_key)
        self.client = openai.OpenAI(api_key=self.api_key)
        
        try:
            self.encoding = tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            logger.warning(f"Model '{self.model_name}' not found for tiktoken. Falling back to 'cl100k_base'.")
            self.encoding = tiktoken.get_encoding("cl100k_base")
            
        self.MAX_INPUT_TOKENS = 120000 # Safe margin from 8k limit

    def _get_token_count(self, text: str) -> int:
        return len(self.encoding.encode(text, disallowed_special=()))

    def extract(self, consolidated_text: str) -> list[dict]:
        """
        Analyzes consolidated text from a documentation site to extract modules.
        """
        if not consolidated_text.strip():
            logger.warning("Extractor received empty text. Nothing to process.")
            return []

        # Pass 1: Extract raw modules from chunks of the text.
        logger.info("Starting Pass 1: Raw module extraction.")
        raw_modules_json_string = self._extract_raw_modules_from_chunks(consolidated_text)
        
        if not raw_modules_json_string or raw_modules_json_string == "[]":
            logger.warning("Pass 1 did not yield any modules.")
            return []
            
        # Pass 2: Synthesize and clean the raw modules.
        logger.info("Starting Pass 2: Synthesizing and cleaning modules.")
        final_modules = self._synthesize_and_clean_modules(raw_modules_json_string)
        
        return final_modules

    def _extract_raw_modules_from_chunks(self, text: str) -> str:
        """
        Takes large text, chunks it, calls the LLM on each chunk for raw extraction,
        and returns a JSON string of the combined, messy results.
        """
        chunks = self._chunk_text_by_tokens(text, self.MAX_INPUT_TOKENS)
        all_raw_modules = []
        
        extraction_prompt = self._get_extraction_prompt()
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)} in Pass 1.")
            response_text = self._call_llm(chunk, extraction_prompt)
            parsed_chunk_modules = self._parse_llm_output(response_text)
            if parsed_chunk_modules:
                all_raw_modules.extend(parsed_chunk_modules)
                
        return json.dumps(all_raw_modules, indent=2)

    def _synthesize_and_clean_modules(self, raw_modules_json: str) -> list[dict]:
        """
        Takes a JSON string of messy modules and asks the LLM to clean,
        merge, and de-duplicate them into a final list.
        """
        num_tokens = self._get_token_count(raw_modules_json)
        if num_tokens > self.MAX_INPUT_TOKENS:
            logger.warning(f"Cannot perform synthesis pass: raw module data is too large ({num_tokens} tokens). Returning raw data.")
            return json.loads(raw_modules_json) # Fallback to returning messy data

        synthesis_prompt = self._get_synthesis_prompt()
        final_response_text = self._call_llm(raw_modules_json, synthesis_prompt)
        final_modules = self._parse_llm_output(final_response_text)
        
        return final_modules

    def _get_extraction_prompt(self) -> str:
        return """
        You are an AI assistant analyzing a piece of website documentation. Your task is to identify and extract any product features (modules) and their specific functionalities (submodules) from the provided text.
        Structure your output as a valid JSON. The JSON should be a list of objects.
        Each object must have "module" (string), "Description" (string), and "Submodules" (an object).
        Extract information ONLY from the provided text. If you find no modules, return an empty list [].
        """

    def _get_synthesis_prompt(self) -> str:
        return """
        You are a data synthesis AI. You will be given a JSON list of "modules" extracted from a website's documentation. This list is messy, containing many duplicates, fragments, and overlapping information because it was generated from small chunks of the full text.
        Your task is to process this entire JSON list and produce a single, clean, de-duplicated, and logically structured final JSON list of modules.
        - Merge duplicate modules (e.g., "Account Settings" and "Settings, Account").
        - Combine descriptions for the same module to be more comprehensive.
        - Merge submodules for the same module and de-duplicate them.
        - Remove any irrelevant or clearly non-module entries.
        - Ensure the final output is a valid JSON list of objects, with "module", "Description", and "Submodules" keys.
        """

    def _call_llm(self, content: str, system_prompt: str) -> str:
        """Makes a call to the OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            return response.choices[0].message.content
        except openai.APIStatusError as e:
            logger.error(f"OpenAI API status error: {e.status_code} - {e.response.text}")
            return ""
        except Exception as e:
            logger.error(f"An unexpected error occurred during LLM call: {e}")
            return ""

    def _parse_llm_output(self, response_text: str) -> list[dict]:
        """
        Parses the JSON string from the LLM. Handles cases where the LLM
        returns a single object instead of a list.
        """
        if not response_text:
            return []
        try:
            data = json.loads(response_text)
            
            if isinstance(data, list):
                return data
            
            if isinstance(data, dict):
                # If the dict contains a list, return that.
                for key, value in data.items():
                    if isinstance(value, list):
                        return value
                # If the dict is a single module, wrap it in a list.
                if 'module' in data and 'Description' in data:
                    logger.warning("LLM returned a single module object, wrapping it in a list.")
                    return [data]
            
            logger.warning(f"Could not parse a valid module list from LLM response: {response_text}")
            return []
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from LLM response: {response_text}")
            return []

    def _chunk_text_by_tokens(self, text: str, max_tokens: int) -> list[str]:
        """Splits text into chunks, each not exceeding max_tokens."""
        text_blocks = text.split('\n\n')
        chunks, current_chunk_blocks, current_chunk_tokens = [], [], 0

        for block in text_blocks:
            block_tokens = self._get_token_count(block)
            if block_tokens > max_tokens:
                if current_chunk_blocks:
                    chunks.append("\n\n".join(current_chunk_blocks))
                    current_chunk_blocks, current_chunk_tokens = [], 0
                
                # Force-split the oversized block
                char_limit = max_tokens * 3  # Approx chars per token, with a safety margin
                for i in range(0, len(block), char_limit):
                    chunks.append(block[i:i + char_limit])
                continue

            if current_chunk_tokens + block_tokens > max_tokens and current_chunk_blocks:
                chunks.append("\n\n".join(current_chunk_blocks))
                current_chunk_blocks, current_chunk_tokens = [], 0

            current_chunk_blocks.append(block)
            current_chunk_tokens += self._get_token_count("\n\n".join(current_chunk_blocks))
        
        if current_chunk_blocks:
            chunks.append("\n\n".join(current_chunk_blocks))
        
        logger.info(f"Content was split into {len(chunks)} chunk(s).")
        return chunks