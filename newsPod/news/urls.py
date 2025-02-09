from django.urls import path
from .views import home, save_news, saved_news

urlpatterns = [
    path("", home, name="home"),
    path("save/", save_news, name="save_news"),
    path("saved/", saved_news, name="saved_news"),
]
