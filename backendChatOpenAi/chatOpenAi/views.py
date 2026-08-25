import logging

from django.conf import settings
from openai import OpenAI, OpenAIError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieRecommendationSerializer, RecommendationRequestSerializer


logger = logging.getLogger(__name__)


def generate_recommendation(user_input: str) -> str:
    """Call the external API in one place so tests can replace the network boundary."""

    client = OpenAI(api_key=settings.OPENAI_API_KEY, max_retries=1, timeout=20.0)
    completion = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente especializado en películas. Responde en "
                    "español y menciona títulos concretos de forma breve."
                ),
            },
            {
                "role": "user",
                "content": f"Recomienda una película según esta preferencia: {user_input}",
            },
        ],
        max_tokens=150,
    )
    return (completion.choices[0].message.content or "").strip()


@api_view(["GET"])
def health(request):
    """Dependency-free endpoint for students and Docker healthchecks."""

    return Response({"status": "ok"})


@api_view(["POST"])
def recommend_movie(request):
    serializer = RecommendationRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if not settings.OPENAI_API_KEY:
        return Response(
            {
                "error": (
                    "OPENAI_API_KEY no está configurada. Consulta .env.example "
                    "y reinicia el servidor."
                )
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    try:
        recommendation = generate_recommendation(serializer.validated_data["message"])
    except OpenAIError:
        logger.exception("The OpenAI request failed")
        return Response(
            {"error": "No fue posible obtener una recomendación en este momento."},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    matched_movies = [
        movie
        for movie in Movie.objects.all()
        if movie.title.casefold() in recommendation.casefold()
    ][:3]

    if matched_movies:
        movies = MovieRecommendationSerializer(matched_movies, many=True).data
        return Response(
            {
                "response": (
                    "Puedo recomendarte estas películas según lo que mencionaste: "
                    f"{recommendation}"
                ),
                "movies": movies,
            }
        )

    return Response(
        {
            "response": (
                "No encontré el título recomendado en el catálogo local, pero la "
                f"recomendación fue: {recommendation}"
            ),
            "movies": [],
        }
    )
