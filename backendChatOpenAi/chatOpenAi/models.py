from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    image_url = models.URLField()
    description = models.TextField()

    class Meta:
        ordering = ["title", "genre"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "genre"], name="unique_movie_title_genre"
            )
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.genre})"
