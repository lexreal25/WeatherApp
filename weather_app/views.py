from django.shortcuts import render
import requests
import datetime
import asyncio

def index(request):
    api_key = '5f0cd6d886876a3e4c9ae04f36c81c68'
    #current_weather_url = 'https://api.openweathermap.org/data/3.0/weather?q={}&appid={}'
    current_weather_url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'
    #forecast_url='api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    try:
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    except:
        print('Error')
      
    weather_data = {
        'city': response['name'],
        'temperature': round(response['main']['temp'] - 273.15),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
        'day': datetime.datetime.fromtimestamp(response['dt']).strftime('%A')
    }

    daily_forecasts = []
    for daily_data in forecast_response['list'][:4]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'date':daily_data['dt_txt'].split(' ')[0],
            'time':daily_data['dt_txt'].split(' ')[1],
            'min_temp': round(daily_data['main']['temp_min'] - 273.15),
            'max_temp': round(daily_data['main']['temp_max'] - 273.15),
            'description': daily_data['weather'][0]['description'],
            'main':daily_data['weather'][0]['main'],
            'icon': daily_data['weather'][0]['icon'],
            'wind_speed':daily_data['wind']['speed'],
        })

    return weather_data,daily_forecasts
