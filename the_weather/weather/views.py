import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests
import json
from math import sin, cos, sqrt, atan2, radians

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=20e84c6dbae34e0d6ece4c8f8d0f4314'

    search = None
    if request.method == 'POST':
        search = request.POST.get('name','') # https://stackoverflow.com/questions/4162625/django-request-get-parameters
        #print(city) # this is just for testing: you can remove it when done.
        # Doesn't save to database, but still loads from database.
        #form.save()

    url2 = 'https://records.nhl.com/site/api/franchise'
    response2 = requests.get(url2).json()
    team_dicts = response2['data']

    team_id = None
    for d in team_dicts:
        if( d['teamPlaceName'] == search or 
            d['teamCommonName'] == search or 
            d['teamPlaceName'] + ' ' +d['teamCommonName'] == search ):
            team_id = d['mostRecentTeamId']
    
    team_data_url = 'https://records.nhl.com/site/api/team'
    team_response = requests.get(team_data_url).json()
    team_stats = team_response['data']
    
    displayTeamName = None
    ticketsURL = None
    arenaCoords = None
    distance = None
    for team in team_stats:
        if (team['teamId']==team_id):
            print("Team Name: " + team['fullName'] + " Active: " + team['active'] + " Arena Address: " + team['arenaAddress'])
            displayTeamName = team['fullName']
            ticketsURL = team['buySellTicketUrl']
            arenaCoords = team['arenaCoordinates'].split(",")

            response_data = requests.get('https://www.iplocation.net/go/ipinfo').text
            response_json_data = json.loads(response_data)
            location = response_json_data["loc"].split(",")
            print(arenaCoords[1])
            R = 6373.0
            lat1 = radians(float(location[0]))
            lon1 = radians(float(location[1]))
            lat2 = radians(float(arenaCoords[0]))
            lon2 = radians(float(arenaCoords[1]))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            distance = round(distance,2)
            print("Result:", distance)

    #https://stackoverflow.com/questions/45630606/can-i-get-accurate-geolocation-in-python-using-html5-location-tool
 

    #https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude



    #print(response2)


    #final = r2['data'][0]['data']

    #print(final)


    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : displayTeamName,
            'temperature' : "Distance from Current Location to Arena: " + str(distance),
            'description' : ticketsURL,
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)
