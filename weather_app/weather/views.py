from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.

def index(request):
    #url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
    #city = 'Bengaluru'

    error_msg = ''
    user_msg = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            current_city_count = City.objects.filter(name=new_city).count()
            
            if current_city_count == 0:
                res = requests.get(url.format(new_city)).json()
                #print(res)
                if res['cod'] == 200:
                    form.save()
                else:
                    error_msg = 'Invalid City. It does not exist.'
            else:
                error_msg = 'Duplicate entry. City is already present in DB.'

        if error_msg:
            user_msg = error_msg
            message_class = 'is-danger'
        else:
            user_msg = 'City added successfully.'
            message_class = 'is-success'
    
    #print(error_msg)
    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        res = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temp' : res['main']['temp'],
            'desc' : res['weather'][0]['description'],
            'icon' : res['weather'][0]['icon']
            }
            
        weather_data.append(city_weather)

    print(weather_data)
    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'user_msg' : user_msg,
        'message_class' : message_class
    }

    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')