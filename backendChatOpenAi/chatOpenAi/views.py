import openai
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os
from .movie_list import MOVIE_LIST

# Configure your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@api_view(['POST'])
def recommend_movie(request):
    user_input = request.data.get('message', '')

    try:
        if not openai.api_key:
            raise ValueError("The OpenAI API key is not set.")
        
        # Fetch response from OpenAI based on user input
        client = openai.OpenAI(api_key=openai.api_key)
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Recomienda una película o responde de manera coherente sobre esto: {user_input}"}
            ],
            max_tokens=150
        )
        
        recommendation = completion.choices[0].message.content.strip()
        print(f"OpenAI Recommendation: {recommendation}")

        # Attempt to find up to 3 movie matches
        matched_movies = [
            movie for movie in MOVIE_LIST 
            if movie['title'].lower() in recommendation.lower()
        ][:3] # Limit to 3 recommendations

        if matched_movies:
            response_text = f"Puedo recomendarte estas películas en base a lo que mencionaste: {recommendation}"
            return JsonResponse({'response': response_text, 'movies': matched_movies})
        else:
            # Generic response when no movie match is found
            return JsonResponse({
                'response': f"No estoy preparado para responder otro tipo de preguntas, pero: {recommendation}"
                #'response': f"Recuerda que solo puedo responder con informacion relacionada a nuestra base de datos de peliculas"
            })
    except Exception as e:
        return JsonResponse({'error': f'Error processing request: {str(e)}'})
    