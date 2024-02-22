# This Python file uses the following encoding: utf-8
import logging
from configparser import ConfigParser
from phue import Bridge


def _get_bridge_ip():
    config = ConfigParser()
    config.read('secrets.ini')
    return config['hue']['bridge_ip']

def _connect_with_bridge():
    b = Bridge(_get_bridge_ip())

    try:
        b.connect()
    except Exception as e:
        logging.error(e)
        return None

    return b.get_light_objects()

def _print_available_lights():
    print('Available lights:')
    for light in lights:
        print(f'- {light.name} ({light.light_id})')

def turn_on_lights(brightness: int = 100) -> bool:
    lights = _connect_with_bridge()

    if lights:
        for light in lights:
            light.on = True
            light.brightness = brightness
            light.xy = (0.5, 0.4)
            light.effect = None
        return True

    return False

def turn_off_lights() -> bool:
    lights = _connect_with_bridge()

    if lights:
        for light in lights:
            light.on = False
        return True
    return False

def turn_on_color_loop() -> bool:
    lights = _connect_with_bridge()

    if lights:
        for light in lights:
            light.on = True
            light.brightness = 30
            light.transitiontime = 100
            light.effect = 'colorloop'
        return True

    return False
