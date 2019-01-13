import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    url = 'https://records.nhl.com/site/api/franchise'
    
    
    
    """
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
    """
    

    #context = {'weather_data' : weather_data, 'form' : form}
    response = requests.get(url).json()
    #final = r['data'][0]['data']
    
    response = response['data']
    return JsonResponse(response, safe=False)
    
    

    #return HttpResponse(final)
    #return JsonResponse(final)
    #render(request, 'weather/weather.html', context)
