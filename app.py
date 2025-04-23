from flask import Flask, request, jsonify, send_from_directory, render_template
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from summarizer import summarize_text
from scraper import scrape_category
from db import get_article_by_url
from config import IMAGE_FOLDER
from logger import logger  # Import logger

# Initialize Flask app with static and template folders
app = Flask(__name__, static_folder='static', template_folder='templates')


# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def home():
    """
    Home route to serve the main frontend page.
    """
    logger.info("Home page served.")
    return render_template("index.html")


@app.route('/scrape', methods=['POST'])
def scrape():
    """
    Scrapes articles from a provided Geo TV category URL.
    Returns the list of newly scraped article URLs.
    """
    data = request.json
    category_url = data.get("url")
    if not category_url:
        logger.warning("Scrape request missing category URL.")
        return jsonify({"error": "Missing category URL"}), 400

    logger.info(f"Starting scrape for category: {category_url}")
    scraped_urls = scrape_category(category_url)
    logger.info(f"Scraped {len(scraped_urls)} new articles.")

    return jsonify({
        "message": f"✅ Scraped {len(scraped_urls)} new articles.",
        "scraped_urls": scraped_urls
    })


@app.route('/fetch', methods=['POST'])
def fetch():
    """
    Retrieves a specific article from the database using its URL.
    Returns title, date, full text, and image path.
    """
    data = request.json
    article_url = data.get("url")
    if not article_url:
        logger.warning("Fetch request missing article URL.")
        return jsonify({"error": "Missing article URL"}), 400

    logger.info(f"Fetching article from DB for URL: {article_url}")
    article = get_article_by_url(article_url)
    if not article:
        logger.warning(f"Article not found in DB for URL: {article_url}")
        return jsonify({"error": "Article not found"}), 404

    image_path = article.get("image_path")
    image_url = f"/images/{os.path.basename(image_path)}" if image_path else None
    date = article.get("date", "")
    display_date = date.split("T")[0] if "T" in date else date

    logger.info(f"Article retrieved successfully: {article_url}")
    return jsonify({
        "title": article.get("title"),
        "date": display_date,
        "text": article.get("text"),
        "image_path": image_url,
    })


@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Accepts article text and returns a summarized version.
    """
    data = request.json
    text = data.get("text")
    if not text:
        logger.warning("Summarize request missing article text.")
        return jsonify({"error": "Missing article text"}), 400

    logger.info("Generating summary for provided text.")
    summary = summarize_text(text)
    logger.info("Summary generated successfully.")
    return jsonify({"summary": summary})


@app.route('/images/<filename>')
def serve_image(filename):
    """
    Serves images stored locally on the VM.
    """
    logger.info(f"Serving image: {filename}")
    return send_from_directory(IMAGE_FOLDER, filename)


# ----------------------------
# ENTRY POINT
# ----------------------------

if __name__ == "__main__":
    logger.info("Starting Flask app on port 8000...")
    app.run(host="0.0.0.0", port=8000)
