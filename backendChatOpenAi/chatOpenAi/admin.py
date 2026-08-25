from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "short_description")
    list_filter = ("genre",)
    search_fields = ("title", "description")
    ordering = ("title", "genre")

    @admin.display(description="Descripción")
    def short_description(self, movie: Movie) -> str:
        return movie.description[:80]
