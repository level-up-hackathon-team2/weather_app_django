import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=20e84c6dbae34e0d6ece4c8f8d0f4314'





    city = None
    if request.method == 'POST':
        city = request.POST.get('name','') # https://stackoverflow.com/questions/4162625/django-request-get-parameters
        print(city) # this is just for testing: you can remove it when done.
        # Doesn't save to database, but still loads from database.
        #form.save()

    url2 = 'https://records.nhl.com/site/api/franchise'

    response2 = requests.get(url2).json()

    team_dicts = response2['data']

    team_id = None
    for d in team_dicts:
        if(d['teamPlaceName'] == city):
            team_id = d['mostRecentTeamId']
    

    team_data_url = 'https://records.nhl.com/site/api/team'

    team_response = requests.get(team_data_url).json()

    team_stats = team_response['data']
    
    displayTeamName = None
    ticketsURL = None
    for team in team_stats:
        if (team['teamId']==team_id):
            print("Team Name: " + team['fullName'] + " Active: " + team['active'] + " Arena Address: " + team['arenaAddress'])
            displayTeamName = team['fullName']
            ticketsURL = team['buySellTicketUrl']

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
            'temperature' : r['main']['temp'],
            'description' : ticketsURL,
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)
