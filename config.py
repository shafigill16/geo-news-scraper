import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")  # ← Updated to use container hostname
DB_NAME = os.getenv("DB_NAME", "geo_news")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "articles")
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "/app/images")
