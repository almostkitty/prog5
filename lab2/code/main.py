import os
import json
from dotenv import load_dotenv
from getweatherdata import get_weather_data


load_dotenv()
api_key = os.getenv('owm_api_key')

if __name__ == '__main__':
    cities = ['Moscow', 'Saint Petersburg', 'Los Angeles', 'Athens']
    
    for city in cities:
        try:
            weather_data = get_weather_data(city, api_key)
            print(f"Погода в {city}:")
            print(weather_data)
            #print(json.dumps(weather_data, indent=4, ensure_ascii=False))
            print()
        except Exception as e:
            print(f"Произошла ошибка при получении данных для {city}: {e}")
