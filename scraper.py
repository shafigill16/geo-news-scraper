from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
from urllib.parse import urlparse, urljoin

from config import IMAGE_FOLDER
from db import article_exists, save_article
from logger import logger  # Logging setup

# Define headers for HTTP requests to avoid being blocked by the server
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def download_image(img_url):
    """
    Downloads an image from the given URL and saves it to the local IMAGE_FOLDER.
    Returns the local file path if successful, or None on failure.
    """
    try:
        response = requests.get(img_url, headers=HEADERS, stream=True)
        if response.status_code == 200:
            filename = os.path.basename(urlparse(img_url).path)
            file_path = os.path.join(IMAGE_FOLDER, filename)

            # Save image in chunks to avoid memory issues
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            logger.info(f"Downloaded image: {img_url} -> {file_path}")
            return file_path
        else:
            logger.warning(f"Failed to download image: {img_url} - Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Image download error: {img_url} - {e}")

    return None


def scrape_article(url):
    """
    Scrapes a single article page to extract title, date, content, and image.
    Stores the article in the database if not already present.
    Returns article data if new, otherwise None.
    """
    if article_exists(url):
        logger.info(f"Article already exists: {url}")
        return None

    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract article title
        title = soup.select_one(".heading_H h1").get_text(strip=True)

        # Extract and format date
        raw_date = soup.select_one(".post-date-time").text.strip()
        date_obj = datetime.strptime(raw_date, "%B %d, %Y")
        date = date_obj.isoformat()

        # Extract main text content
        paragraphs = soup.select(".content-area p")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs)

        # Extract image and download locally
        image_tag = soup.select_one(".medium-insert-images img")
        img_url = image_tag["src"] if image_tag else None
        image_path = download_image(img_url) if img_url else None

        # Combine data into a dictionary
        article_data = {
            "url": url,
            "title": title,
            "date": date,
            "text": text,
            "image_path": image_path,
        }

        save_article(article_data)
        logger.info(f"Scraped and saved article: {url}")
        return article_data

    except Exception as e:
        logger.error(f"Failed to scrape article: {url} - {e}")
        return None


def scrape_category(category_url):
    """
    Scrapes all valid article links from a Geo TV category page.
    Calls scrape_article on each new URL and skips duplicates.
    Returns a list of successfully scraped article URLs.
    """
    logger.info(f"Scraping category: {category_url}")
    scraped_urls = []

    try:
        response = requests.get(category_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        # Select all article links
        links = soup.select("a.open-section")
        article_urls = set()

        for link in links:
            href = link.get("href")
            if href and "/latest/" in href:
                full_url = urljoin(category_url, href)
                article_urls.add(full_url)

        logger.info(f"Found {len(article_urls)} potential article URLs.")

        # Scrape each article if not already in DB
        for url in article_urls:
            if not article_exists(url):
                result = scrape_article(url)
                if result:
                    scraped_urls.append(url)

        logger.info(f"✅ Scraped {len(scraped_urls)} new articles.")
        return scraped_urls

    except Exception as e:
        logger.error(f"❌ Error during category scraping: {e}")
        return []
