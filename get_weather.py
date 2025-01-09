import os
import requests

from dotenv import load_dotenv


def get_weather(api_key: str, city: str) -> dict:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(url)
    except Exception as exp:
        print(exp)
        return {}
    
    if response.status_code == 200:

        data = response.json()
        
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        temperature_feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        weather_data = {'temperature': temperature,
                        'temperature_feels_like': temperature_feels_like,
                        'humidity': humidity,
                        'wind_speed': wind_speed,
                        'weather_description': weather_description
                        }
        return weather_data
    return {}


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get('API_KEY')
    city = 'Malahide'

    get_weather(api_key, city)
