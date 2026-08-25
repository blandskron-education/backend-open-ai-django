from django.core.management.base import BaseCommand

from chatOpenAi.models import Movie
from chatOpenAi.movie_list import MOVIE_LIST


class Command(BaseCommand):
    help = "Carga el catálogo educativo de películas sin crear duplicados."

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for item in MOVIE_LIST:
            _, created = Movie.objects.update_or_create(
                title=item["title"],
                genre=item["genre"],
                defaults={
                    "description": item["overview"],
                    "image_url": item["poster_url"],
                },
            )
            created_count += int(created)
            updated_count += int(not created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Catálogo listo: {created_count} creadas, {updated_count} actualizadas."
            )
        )
