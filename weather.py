from configparser import ConfigParser
from urllib import parse

from settings import CITY, TEMP_UNIT

OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'


def _get_api_key():
    config = ConfigParser()
    config.read('secrets.ini')
    return config['openweather']['api_key']

def build_weather_query():
    api_key = _get_api_key()
    encoded_city = parse.quote_plus(CITY)

    url = f'{OPENWEATHER_API_URL}?q={encoded_city}&units={TEMP_UNIT}&appid={api_key}'

    return url