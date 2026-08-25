from django.urls import path

from .views import health, recommend_movie

app_name = "chatOpenAi"

urlpatterns = [
    path("health/", health, name="health"),
    path("recommend/", recommend_movie, name="recommend"),
]
