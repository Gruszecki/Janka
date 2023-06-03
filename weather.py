import datetime
import json
import logging
import sys
import time
from configparser import ConfigParser
from typing import Union
from urllib import parse, request, error

from settings import CITY, TEMP_UNIT

OPENWEATHER_API_CURRENT_URL = 'https://api.openweathermap.org/data/2.5/weather'
OPENWEATHER_API_FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'


def _get_api_key():
    config = ConfigParser()
    config.read('secrets.ini')
    return config['openweather']['api_key']

def _build_weather_query(mode: str) -> Union[str, None]:
    api_key = _get_api_key()
    encoded_city = parse.quote_plus(CITY)

    match mode:
        case 'current':
            URL = OPENWEATHER_API_CURRENT_URL
            url = f'{URL}?q={encoded_city}&units={TEMP_UNIT}&lang=pl&appid={api_key}'
        case 'forecast':
            URL = OPENWEATHER_API_FORECAST_URL
            url = f'{URL}?q={encoded_city}&cnt=8&units={TEMP_UNIT}&lang=pl&appid={api_key}'
        case _:
            url = None

    return url

def get_weather_raw_data(mode: str) -> Union[json, None]:
    """
    Get weather data from OpenWeatherMap API.
    :param mode: 'current' for current weather or 'forecast' for daily weather
    :return: json or None
    """
    query = _build_weather_query(mode)
    print(query)

    try:
        response = request.urlopen(query)
        data = response.read()
        weather_data = json.loads(data)

    except error.HTTPError as http_error:
        match http_error.code:
            case 401:
                logging.error(' No weather access. The API key may be expired.')
            case 404:
                logging.error(f' No weather found for the city: {CITY}.')
        weather_data = None

    except json.JSONDecodeError:
        logging.error(' Cannot parse server response.')
        weather_data = None

    return weather_data


def get_current_weather_full_deccription() -> str:
    local_time = time.localtime(time.time())
    weather_data = get_weather_raw_data('current')

    if weather_data:
        weather_desc = f'Pogoda dla miejscowości {CITY}. Stan na godzinę {local_time.tm_hour}:{str(local_time.tm_min).zfill(2)}. ' \
                       f'{weather_data["weather"][0]["description"]}. ' \
                       f'Temperatura wynosi {weather_data["main"]["temp"]} stopni Celsjusza. ' \
                       f'Temperatura odczuwalna: {weather_data["main"]["feels_like"]} stopni Celsjusza. ' \
                       f'Zachmurzenie {weather_data["clouds"]["all"]}%. ' \
                       f'Prędkość wiatru {weather_data["wind"]["speed"]} m/s. ' \
                       f'Wilgotność powietrza {weather_data["main"]["humidity"]}%. ' \
                       f'Wschód słońca: {time.localtime(weather_data["sys"]["sunrise"]).tm_hour}:{str(time.localtime(weather_data["sys"]["sunrise"]).tm_min).zfill(2)}. ' \
                       f'Zachód słońca: {time.localtime(weather_data["sys"]["sunset"]).tm_hour}:{str(time.localtime(weather_data["sys"]["sunset"]).tm_min).zfill(2)}.'

        return weather_desc
    else:
        return 'W tej chwili pogoda jest niedostępna.'

def get_raw_daily_forecast():
    morn = None
    day = None
    eve = None
    night = None

    weather_data = get_weather_raw_data('forecast')

    if weather_data:
        timeshift = weather_data['city']['timezone']//3600

        for entry in weather_data['list']:
            dt = int(entry['dt_txt'].split()[1][:2]) + timeshift

            match dt:
                case 7 | 8 | 9:
                    morn = {
                        'temp': entry['main']['temp'],
                        'desc': entry['weather'][0]['description']
                    }
                case 11 | 12 | 13:
                    day = {
                        'temp': entry['main']['temp'],
                        'desc': entry['weather'][0]['description']
                    }
                case 17 | 18 | 19:
                    eve = {
                        'temp': entry['main']['temp'],
                        'desc': entry['weather'][0]['description']
                    }
                case 2 | 3 | 4:
                    night = {
                        'temp': entry['main']['temp'],
                        'desc': entry['weather'][0]['description']
                    }

            if 2 <= dt <= 4 :  # We reached to the end of the day (night actually)
                break
    else:
        logging.error(' Weather forecast is not available right now.')

    return morn, day, eve, night

def get_daily_forecast():
    morn, day, eve, night = get_raw_daily_forecast()

    if any([morn, day, eve, night]):
        full_string = ''
        if morn:
            full_string += f'Rano: {morn["temp"]} stopni Celsjusza. {morn["desc"]}. '
        if day:
            full_string += f'W południe: {day["temp"]} stopni Celsjusza. {day["desc"]}. '
        if eve:
            full_string += f'Wieczorem: {eve["temp"]} stopni Celsjusza. {eve["desc"]}. '
        if night:
            full_string += f'W nocy: {night["temp"]} stopni Celsjusza. {night["desc"]}. '

        return full_string
    else:
        return 'W tej chwili prognoza pogody jest niedostępna.'
