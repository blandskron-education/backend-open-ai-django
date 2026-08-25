import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from openai import APIConnectionError

from .models import Movie


class MovieModelTests(TestCase):
    def test_string_representation_includes_title_and_genre(self):
        movie = Movie(title="The Matrix", genre="Science Fiction")

        self.assertEqual(str(movie), "The Matrix (Science Fiction)")


class SeedMoviesCommandTests(TestCase):
    def test_seed_is_idempotent(self):
        call_command("seed_movies", verbosity=0)
        first_count = Movie.objects.count()

        call_command("seed_movies", verbosity=0)

        self.assertGreater(first_count, 0)
        self.assertEqual(Movie.objects.count(), first_count)


class EnsureSuperuserCommandTests(TestCase):
    @patch.dict(
        os.environ,
        {
            "DJANGO_SUPERUSER_USERNAME": "teacher",
            "DJANGO_SUPERUSER_EMAIL": "teacher@example.com",
            "DJANGO_SUPERUSER_PASSWORD": "educational-password",
        },
        clear=False,
    )
    def test_command_creates_user_only_once(self):
        call_command("ensure_superuser", verbosity=0)
        call_command("ensure_superuser", verbosity=0)

        users = get_user_model().objects.filter(username="teacher")
        self.assertEqual(users.count(), 1)
        self.assertTrue(users.get().is_superuser)


class RecommendationApiTests(TestCase):
    def setUp(self):
        self.url = reverse("chatOpenAi:recommend")
        Movie.objects.create(
            title="The Matrix",
            genre="Science Fiction",
            description="A computer hacker discovers the truth about reality.",
            image_url="https://example.com/matrix.jpg",
        )

    def test_health_endpoint(self):
        response = self.client.get(reverse("chatOpenAi:health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_message_is_required(self):
        response = self.client.post(self.url, {}, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json())

    @override_settings(OPENAI_API_KEY="")
    def test_missing_api_key_returns_service_unavailable(self):
        response = self.client.post(
            self.url, {"message": "acción"}, content_type="application/json"
        )

        self.assertEqual(response.status_code, 503)

    @override_settings(OPENAI_API_KEY="test-key")
    @patch("chatOpenAi.views.generate_recommendation", return_value="Mira The Matrix")
    def test_returns_matching_catalog_movie(self, generate_recommendation):
        response = self.client.post(
            self.url, {"message": "ciencia ficción"}, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["movies"][0]["title"], "The Matrix")
        generate_recommendation.assert_called_once_with("ciencia ficción")

    @override_settings(OPENAI_API_KEY="test-key")
    @patch(
        "chatOpenAi.views.generate_recommendation",
        side_effect=APIConnectionError(request=object()),
    )
    def test_openai_failure_returns_bad_gateway(self, generate_recommendation):
        with self.assertLogs("chatOpenAi.views", level="ERROR"):
            response = self.client.post(
                self.url, {"message": "comedia"}, content_type="application/json"
            )

        self.assertEqual(response.status_code, 502)
        self.assertNotIn("test-key", response.content.decode())
