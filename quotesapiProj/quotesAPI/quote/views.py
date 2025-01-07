from django.shortcuts import render
from django.http import JsonResponse
import requests

def index(request):
    return render(request, 'quote/index.html')

def get_quote(request):
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                quote_data = data[0]  # Access the first dictionary in the list
                quote = quote_data.get('q', 'No quote available')
                author = quote_data.get('a', 'Unknown')
                return JsonResponse({'quote': quote, 'author': author})
            else:
                return JsonResponse({'error': 'Unexpected response format from API'})
        else:
            return JsonResponse({'error': f'Failed to fetch quote. Status Code: {response.status_code}'})
    except Exception as e:
        return JsonResponse({'error': str(e)})

