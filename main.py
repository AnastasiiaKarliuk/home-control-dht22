import os
import time
import json
import board
import adafruit_dht

from datetime import datetime
from dotenv import load_dotenv

from get_weather import get_weather


load_dotenv()
api_key = os.environ.get('API_KEY')

sensor = adafruit_dht.DHT22(board.D4)
FREQUENCY_SECS = 120


while True:
    try: 
        date = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = {'temperature': sensor.temperature,
                'humidity': sensor.humidity,
                'date': date}
        data_out = get_weather(api_key=api_key, city='Malahide')
        data["out"] = data_out
        
        with open('sensor_data.txt', 'a') as f:
            f.write(json.dumps(data)+',\n')
            
    except RuntimeError as error:
        time.sleep(2.0)
        continue
    
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(FREQUENCY_SECS)