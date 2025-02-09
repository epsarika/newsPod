import requests
from transformers import pipeline
from gtts import gTTS
import os
from .models import NewsArticle, Category

API_KEY = "827bdde690ce4813bdd2130a41ba15b1"
NEWS_URL = "https://newsapi.org/v2/top-headlines"

summarizer = pipeline("summarization")

def fetch_news(category_name="general"):
    params = {
        "country": "us",
        "category": category_name,
        "apiKey": API_KEY,
    }
    response = requests.get(NEWS_URL, params=params).json()
    
    category, _ = Category.objects.get_or_create(name=category_name)

    for article in response.get("articles", []):
        summary = summarizer(article["content"] or article["description"], max_length=50, min_length=20, do_sample=False)[0]["summary_text"]

        news = NewsArticle.objects.create(
            title=article["title"],
            content=article["content"] or article["description"],
            summary=summary,
            category=category
        )

        tts = gTTS(summary)
        audio_path = f"media/audio/{news.id}.mp3"
        tts.save(audio_path)
        news.audio_file = audio_path
        news.save()
