from rest_framework import serializers

from .models import Movie


class RecommendationRequestSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=500,
        trim_whitespace=True,
        error_messages={
            "blank": "Escribe qué tipo de película quieres ver.",
            "required": "El campo message es obligatorio.",
        },
    )


class MovieRecommendationSerializer(serializers.ModelSerializer):
    overview = serializers.CharField(source="description")
    poster_url = serializers.URLField(source="image_url")

    class Meta:
        model = Movie
        fields = ("title", "genre", "overview", "poster_url")
