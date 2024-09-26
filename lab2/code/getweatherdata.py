import requests
import os


def get_weather_data(place, api_key=None):
    if not api_key:
        return None
    if not place:
        return None
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Ошибка: {response.status_code}, {response.text}")
    

    data = response.json()

    city_name = data['name']
    country_code = data['sys']['country']
    lat = data['coord']['lat']
    lon = data['coord']['lon']
    feels_like = data['main']['feels_like']
    timezone = data['timezone']

    timezone_hours = timezone // 3600
    timezone_str = f"UTC{'+' if timezone_hours >= 0 else '-'}{abs(timezone_hours)}"

    result = {
        "name": city_name,
        "coord": {"lon": lon, "lat": lat},
        "country": country_code,
        "feels_like": feels_like,
        "timezone": timezone_str
    }

    return result
