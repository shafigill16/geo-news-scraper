import requests
import os
from dotenv import load_dotenv
from logger import logger  # Logging setup


# Load environment variables from .env
load_dotenv()

HF_API_URL = os.getenv("HF_API_URL")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MAX_INPUT_CHARS = 5000  # ~1024 tokens


def summarize_text(text):
    """
    Summarizes the input text using Hugging Face API.
    Handles token length limits by specifying truncation.

    Args:
        text (str): The text to summarize.

    Returns:
        str: The summarized text or error message.
    """
    logger.info("Starting text summarization.")
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }

    # Truncate text to avoid exceeding token limits
    text = text[:MAX_INPUT_CHARS]
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 500,
            "min_length": 30,
            "do_sample": False
        },
        "options": {
            "use_cache": True,
            "wait_for_model": True
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)

        if response.status_code != 200:
            logger.error(f"Summarization API error: {response.json()}")
            return f"Error: {response.json()}"

        result = response.json()
        summary = result[0]["summary_text"]
        logger.info("Summarization completed successfully.")
        return summary

    except Exception as e:
        logger.exception(f"Exception during summarization: {e}")
        return f"Error: {str(e)}"
