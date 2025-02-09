from django.db import models
from django.contrib.auth.models import User
from news.models import NewsArticle

class SavedNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news_article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.news_article.title}"
