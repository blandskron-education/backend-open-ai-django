import openai
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os

# Configura tu clave de API de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Example static movie list
MOVIE_LIST = [
    {
        "title": "John Wick",
        "genre": "Action",
        "overview": "An ex-hitman comes out of retirement to track down the gangsters that killed his dog and stole his car.",
        "poster_url": "https://image.tmdb.org/t/p/w500/qIegbn6DSUYmggfwxOBNOVS35q.jpg"
    },
    {
        "title": "The Matrix",
        "genre": "Science Fiction",
        "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "poster_url": "https://image.tmdb.org/t/p/w500/vxuoMW6YBt6UsxvMfRNwRl9LtWS.jpg"
    },
    {
        "title": "Inception",
        "genre": "Science Fiction",
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "poster_url": "https://image.tmdb.org/t/p/w500/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg"
    }
]

@api_view(['POST'])
def recommend_movie(request):
    user_input = request.data.get('message', '')

    try:
        if not openai.api_key:
            raise ValueError("The OpenAI API key is not set.")
        
        # Fetch movie recommendation from OpenAI
        client = openai.OpenAI(api_key=openai.api_key)
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Recomienda una película o serie basada en: {user_input}"}
            ],
            max_tokens=150
        )
        
        recommendation = completion.choices[0].message.content.strip()
        print(f"OpenAI Recommendation: {recommendation}")

        # Search for a movie in the static list
        selected_movie = next(
            (movie for movie in MOVIE_LIST if movie['title'].lower() in recommendation.lower()), 
            None
        )

        if selected_movie:
            return JsonResponse({'response': recommendation, 'movie': selected_movie})
        else:
            return JsonResponse({'error': 'No matching movie found in the static list.', 'openai_response': recommendation})
    except Exception as e:
        return JsonResponse({'error': f'Error processing request: {str(e)}'})
    