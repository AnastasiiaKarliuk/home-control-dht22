import os
import time
import json
import board
import requests
import adafruit_dht

from datetime import datetime
from dotenv import load_dotenv
from influxdb import InfluxDBClient

from get_weather import get_weather

load_dotenv()
api_key = os.environ.get('API_KEY')

db_host = os.environ.get('INFLUX_DB_HOST')
db_port = int(os.environ.get('INFLUX_DB_PORT'))
db_username = os.environ.get('INDLUX_DB_USERNAME')
db_password = os.environ.get('INFLUX_DB_PASSWORD')
db_database = os.environ.get('INFLUX_DB_DATABASE')

client_influx = InfluxDBClient(db_host, db_port, db_username, db_password, db_database)

sensor = adafruit_dht.DHT22(board.D4)
FREQUENCY_SECS = 120


while True:
    try: 
        date = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
        data_inside = {'temperature': sensor.temperature,
                       'humidity': sensor.humidity,
                       'date': date}
        data_out = get_weather(api_key=api_key, city='Malahide')
        data = {**data_inside, **{"out": data_out}}
        
        with open('sensor_data.txt', 'a') as f:
            f.write(json.dumps(data)+',\n')
        
        data_out = {'out_'+k: v for k, v in data_out.items()}

        data_influx = {
            "measurement": "sensor_data",
            "time": datetime.now(),
            "fields": {**data_inside, **data_out}
        }
        client_influx.write_points([data_influx])
        
    except RuntimeError as error:
        time.sleep(2.0)
        continue
    
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(FREQUENCY_SECS)