from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.contrib import messages
from .models import city
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=92bb398a3db301c6f1baa33192501410'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = city.objects.all()
    weather_data = []
    for cities in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': cities.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        if city_weather not in weather_data:
            weather_data.append(city_weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather.html', context)
