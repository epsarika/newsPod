from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to="audio/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="news")
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SavedNews(models.Model):
    title = models.CharField(max_length=500)
    summary = models.TextField()
    url = models.URLField()
    image = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, default="general")  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Saved News"

    def __str__(self):
        return self.title