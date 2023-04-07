from django.shortcuts import render
import requests
import os

YELP_API_KEY = os.getenv('YELP_API_KEY')


def index(request):
    return render(request, 'dateplan/Homepage.html')

def results(request):
    if request.method == 'POST':
        form_data = request.POST
        # process the form data as needed
        search_term = form_data['search_term']
        
        headers = {
            'Authorization': 'Bearer %s' % YELP_API_KEY,
        }
        
        params = {
            'term': search_term,
            'location': 'San Francisco',
            'limit': 5
        }
        
        url = 'https://api.yelp.com/v3/businesses/search'
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return render(request, 'dateplan/results.html', {'data': data})
    else:
        return render(request, 'dateplan/index.html')

