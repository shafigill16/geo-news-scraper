from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from logger import logger  # Import logger for logging

# Connect to MongoDB using the provided URI
logger.info("Connecting to MongoDB...")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
logger.info("Connected to MongoDB.")


def article_exists(url):
    """
    Check if an article with the given URL already exists in the database.

    Args:
        url (str): The URL of the article.

    Returns:
        bool: True if the article exists, False otherwise.
    """
    exists = collection.find_one({"url": url}) is not None
    logger.debug(f"Checked existence for article: {url} - Exists: {exists}")
    return exists


def save_article(article_data):
    """
    Save a new article to the database if it does not already exist.

    Args:
        article_data (dict): Dictionary containing article information.
    """
    if not article_exists(article_data["url"]):
        collection.insert_one(article_data)
        logger.info(f"Article saved: {article_data['url']}")
    else:
        logger.info(f"Article already exists, not saved: {article_data['url']}")


def get_article_by_url(url):
    """
    Retrieve an article from the database using its URL.

    Args:
        url (str): The URL of the article.

    Returns:
        dict or None: The article data without the MongoDB _id field,
                      or None if not found.
    """
    article = collection.find_one({"url": url}, {"_id": 0})
    if article:
        logger.info(f"Article retrieved from DB: {url}")
    else:
        logger.warning(f"Article not found in DB: {url}")
    return article
