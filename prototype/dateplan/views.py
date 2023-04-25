from django.shortcuts import render
from django.shortcuts import redirect

import requests
import os

from datetime import datetime
import time
from django.core import serializers

from django.db import models
from .models import PlanContext
from django.contrib import messages

YELP_API_KEY = os.getenv('YELP_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


def index(request):
    return render(request, 'dateplan/index.html')

def homePage(request):
    return render(request, 'dateplan/Homepage.html')


def get_weather(city, date):
    # Use the current date if the date parameter is empty or None
    if not date:
        date_obj = datetime.now()
    else:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    # Convert the datetime object to a Unix timestamp
    date_timestamp = int(date_obj.strftime('%s'))
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&dt={date_timestamp}&appid={WEATHER_API_KEY}"
    response = requests.get(url).json()
    return response

def user_history(request):
    user_results = PlanContext.objects.filter(user=request.user).order_by('-created_at')
    context = {'user_results': user_results}
    return render(request, 'dateplan/user_history.html', context)

def clear_history(request):
    PlanContext.objects.filter(user=request.user).delete()
    return redirect('dateplan:user_history')


def results(request):
    if request.method == 'POST':
        form_data = request.POST
        # process the form data as needed
        date = form_data['date'] # use for weather prediction in later plan generation
        city = form_data['city'] 
        total_budget = form_data['budget']
        activities = form_data.getlist('activities[]')
        #search_term = form_data['search_term']
        
        headers = {
            'Authorization': 'Bearer %s' % YELP_API_KEY,
        }
        
        activity_data = []
        
        for activity in activities:
            params = {
                'term': activity,
                'location': city,
                'limit': 10
            }
            
            url = 'https://api.yelp.com/v3/businesses/search'
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            for business in data['businesses']:
                business['activityName'] = activity
            
            activity_data.append(data)

        weather_data = get_weather(city, date)
        weather_data['main']['feels_like'] = (int) (weather_data['main']['feels_like'] - 273.15) + 1
        weather_data['main']['min'] = (int) (weather_data['main']['temp_min'] - 273.15) + 1
        weather_data['main']['max'] = (int) (weather_data['main']['temp_max'] - 273.15) + 1
        weather_data['date'] = date
           
        # time data modification, must not change!
        if not date: 
            date = datetime.now().strftime('%Y-%m-%d')
            weather_data['date'] = date
        # data_to_store = UserResult(
        #     searchDate = datetime.now(),
        #     planDate = date,
        #     num = len(activities),
        #     temperature = weather_data['main']['feels_like']
        # )
        # data_to_store.save()
        # result_id = data_to_store.id

        # PlanContext.objects.all().delete()
        # PlanContext.objects.filter(user=request.user).delete()


        if total_budget == "quality":
            # Get the business with the highest rating for each activity
            highest_rated_businesses = []
            for data in activity_data:
                if len(data['businesses']) > 0:
                    highest_rated_businesses.append(max(data['businesses'], key=lambda x: (x['rating'], x.get('review_count', 0))))
                else:
                    highest_rated_businesses.append(None)
            
            context = {
                'weather': weather_data,
                'data': highest_rated_businesses
            }
            context_data = PlanContext(
                user=request.user,
                weather=weather_data,
                data=highest_rated_businesses,
                plan_date=date
            )
            context_data.save()
            return render(request, 'dateplan/results.html', context)
        
        else:
            # Get business with lowest price for each activity
            price_map = {
                '':1,
                '$': 2,
                '$$': 3,
                '$$$': 4,
                # Add more categories if needed
            }

            lowest_price_businesses = []
            for data in activity_data:
                if len(data['businesses']) > 0:
                    filtered_businesses = [b for b in data['businesses'] if b['rating'] >= 2]
                    if filtered_businesses:
                        lowest_price_businesses.append(min(filtered_businesses, key=lambda x: price_map.get(x.get('price'), float('inf'))))
                    else:
                        lowest_price_businesses.append(None)
                else:
                    lowest_price_businesses.append(None)

            lowest_price_businesses.sort(key=lambda x: price_map.get(x.get('price'), float('inf')))
            context = {
                'weather': weather_data,
                'data': lowest_price_businesses
            }

            context_data = PlanContext(
                user=request.user,
                weather=weather_data,
                data=lowest_price_businesses,
                plan_date=date
            )
            context_data.save()
            
            return render(request, 'dateplan/results.html', context)

        
    else:
        return render(request, 'dateplan/index.html')



