from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache import cache
from django.contrib import messages
from .models import SavedNews
import requests
import os
import time
from gtts import gTTS
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the summarization pipeline (using a larger model)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def get_cached_news(category):
    """Get news from cache or fetch from API"""
    cache_key = f'news_{category}'
    cached_news = cache.get(cache_key)
    
    if cached_news:
        return cached_news
        
    news = fetch_news(category)
    cache.set(cache_key, news, 300)  # Cache for 5 minutes
    return news

def fetch_news(category="general"):
    """Fetch news from API"""
    try:
        params = {
            "country": "us",
            "category": category,
            "apiKey": settings.NEWS_API_KEY,
            "pageSize": 16  # Reduced for better performance
        }
        
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params=params,
            timeout=5
        )
        response.raise_for_status()
        return response.json().get("articles", [])
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []

def get_cached_summary(text):
    """Get summary from cache or generate new one"""
    if not text or len(text) < 50:
        return text
        
    cache_key = f'summary_{hash(text)}'
    cached_summary = cache.get(cache_key)
    
    if cached_summary:
        return cached_summary
        
    summary = summarize_text(text)
    cache.set(cache_key, summary, 3600)  # Cache for 1 hour
    return summary

def summarize_text(text):
    """Generate a concise summary of the text in 2 sentences."""
    try:
        # Ensure the text is long enough for summarization
        if len(text.split()) < 30:  # If the text is too short, return it as is
            return text
        
        # Generate a summary with a max_length of 60 words (approx 2 sentences)
        summary = summarizer(text, max_length=60, min_length=20, do_sample=False)[0]
        return summary["summary_text"]
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        return text[:100] + "..."  # Fallback to truncation if summarization fails

def get_cached_audio(news_list):
    """Get audio from cache or generate new one"""
    if not news_list:
        return None
        
    content_hash = hash(str(news_list))
    cache_key = f'audio_{content_hash}'
    cached_audio = cache.get(cache_key)
    
    if cached_audio:
        return cached_audio
        
    audio_url = generate_audio(news_list)
    if audio_url:
        cache.set(cache_key, audio_url, 300)  # Cache for 5 minutes
    return audio_url

def generate_audio(news_list):
    """Generate audio file from the combined news summaries"""
    try:
        text = "Today's top news:\n\n"
        # Keep title and summary separate in audio
        text += "\n\n".join(
            f"Story {i+1}: {n['title']}.\n{n['summary']}" 
            for i, n in enumerate(news_list)
        )

        media_folder = os.path.join(settings.MEDIA_ROOT, "news_audio")
        os.makedirs(media_folder, exist_ok=True)

        filename = f"news_{int(time.time())}.mp3"
        path = os.path.join(media_folder, filename)
        
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(path)
        
        return f"/media/news_audio/{filename}"
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        return None

def delete_old_audios():
    """Delete audio files older than 1 day from the news_audio folder"""
    try:
        media_folder = os.path.join(settings.MEDIA_ROOT, "news_audio")
        now = time.time()
        cutoff = now - 86400  # 86400 seconds = 1 day
        if os.path.exists(media_folder):
            for filename in os.listdir(media_folder):
                filepath = os.path.join(media_folder, filename)
                if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff:
                    os.remove(filepath)
                    logger.info(f"Deleted old audio file: {filepath}")
    except Exception as e:
        logger.error(f"Error deleting old audio files: {e}")

def process_news_item(news):
    """Process single news item"""
    title = news.get('title', '')
    desc = news.get('description', '')
    
    if not title and not desc:
        return None
    
    # Only summarize the description, not the title
    summary = get_cached_summary(desc) if desc else "No description available"
    
    return {
        "title": title or "No title available",
        "summary": summary,
        "url": news.get("url", "#"),
        "image": news.get("urlToImage", ""),
        "source": news.get("source", {}).get("name", "Unknown")
    }

def home(request):
    """Home view with optimized processing"""
    categories = ["general", "business", "technology", "sports", "entertainment", "health"]
    category = request.GET.get("category", "general")
    if category not in categories:
        category = "general"
    
    # Delete old audio files (older than 1 day) before processing new request
    delete_old_audios()
    
    news_articles = get_cached_news(category)
    
    # Process news in parallel
    summarized_news = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(process_news_item, news_articles)
        summarized_news = [r for r in results if r]
    
    # Generate a single audio file for all summaries (with caching)
    audio_file = get_cached_audio(summarized_news)
    
    context = {
        "news_articles": summarized_news,
        "categories": categories,
        "selected_category": category,
        "audio_file": audio_file
    }
    
    return render(request, "news/home.html", context)

def save_news(request):
    """Save news with validation"""
    if request.method != "POST":
        return redirect("home")
        
    try:
        title = request.POST.get("title")
        if not title:
            messages.error(request, "News title is required")
            return redirect("home")
            
        if not SavedNews.objects.filter(title=title).exists():
            SavedNews.objects.create(
                title=title,
                summary=request.POST.get("summary", ""),
                url=request.POST.get("url", ""),
                image=request.POST.get("image", ""),
                category=request.POST.get("category", "general")
            )
            messages.success(request, "News saved successfully")
        else:
            messages.info(request, "News already saved")
    except Exception as e:
        logger.error(f"Error saving news: {e}")
        messages.error(request, "Error saving news")
        
    return redirect("home")

def saved_news(request):
    """Display saved news with caching"""
    category = request.GET.get("category")
    cache_key = f'saved_news_{category or "all"}'
    
    saved_articles = cache.get(cache_key)
    if saved_articles is None:
        if category:
            saved_articles = SavedNews.objects.filter(category=category)
        else:
            saved_articles = SavedNews.objects.all().order_by("-created_at")
        cache.set(cache_key, saved_articles, 60)  # Cache for 1 minute
    
    return render(request, "news/saved_news.html", {
        "saved_articles": saved_articles,
        "selected_category": category,
        "categories": ["general", "business", "technology", "sports", "entertainment", "health"]
    })
