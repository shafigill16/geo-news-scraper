# 📰 Geo News Scraper & Summarizer

This is a full-stack, containerized application that scrapes news articles from [Geo TV](https://www.geo.tv/), stores them in MongoDB, retrieves and displays article data (including locally saved images), and provides AI-powered summarization using Hugging Face models.

## 🚀 Features

- ✅ Web Scraping from any Geo TV category
- ✅ Stores title, date, content, image in MongoDB
- ✅ Skips duplicates using article URL
- ✅ AI Summarization using Hugging Face BART
- ✅ Frontend with HTML/CSS/JS
- ✅ Dockerized with MongoDB and Flask
- ✅ Remote-ready (AWS, GCP, etc.)

## 🗂️ Folder Structure

```
geo-news-scraper/
├── app.py
├── scraper.py
├── summarizer.py
├── db.py
├── config.py
├── logger.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── README.md
├── static/
│   ├── styles.css
│   └── script.js
└── templates/
    └── index.html
```

## ⚙️ .env Format

```
MONGO_URI=mongodb://mongo:27017
DB_NAME=geo_news
COLLECTION_NAME=articles
IMAGE_FOLDER=/app/images
HF_API_URL=https://api-inference.huggingface.co/models/facebook/bart-large-cnn
HF_API_TOKEN=your_huggingface_api_token
LOG_LEVEL=INFO
```

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

Then visit: [http://localhost:8000](http://localhost:8000)

## 📡 Remote Deployment (SSH + SCP)

```bash
ssh -i path/to/key.pem ubuntu@<SERVER_IP>
scp -i path/to/key.pem -r geo-news-scraper ubuntu@<SERVER_IP>:/home/ubuntu/app
```

Then run:

```bash
cd /home/ubuntu/app
docker-compose up --build
```

## 🧪 API Endpoints

- POST `/scrape` → Scrape a category
- POST `/fetch` → Get article by URL
- POST `/summarize` → Summarize text
- GET `/images/<filename>` → Load image

## 👨‍💻 Author

Shafi Ur Rehman · Flask · HuggingFace · Docker · HTML/CSS/JS