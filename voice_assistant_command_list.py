# This Python file uses the following encoding: utf-8
from dataclasses import dataclass


@dataclass
class Command:
    func: str
    commands: list


commands_list = [
    Command(
        func='self._radio_on_specific_station(text)',
        commands=['włącz radio']
    ),
    Command(
        func='self._radio_off()',
        commands=['wyłącz radio']
    ),
    Command(
        func='self._next_station()',
        commands=['następna stacja']
    ),
    Command(
        func='self._prev_station()',
        commands=['poprzednia stacja']
    ),
    Command(
        func='self._turn_on_lights()',
        commands=['włącz światło',
                  'włącz światła']
    ),
    Command(
        func='self._turn_on_soft_lights()',
        commands=['włącz delikatne światło',
                  'włącz delikatne światła',
                  'włącz światło nocne',
                  'włącz światła nocne']
    ),
    Command(
        func='self._turn_off_lights()',
        commands=['wyłącz światło',
                  'wyłącz światła']
    ),
    Command(
        func='self._turn_on_light_color_loop()',
        commands=['włącz pętlę kolorów']
    ),
    Command(
        func='VoiceAssistant.say_time()',
        commands=['która godzina',
                  'jaki mamy czas',
                  'która jest',
                  'jaki jest czas',]
    ),
    Command(
        func='VoiceAssistant.say_current_weather()',
        commands=['jaka jest pogoda',
                  'podaj pogodę']
    ),
    Command(
        func='VoiceAssistant.say_daily_forecast()',
        commands=['jaka będzie pogoda',
                  'prognoza pogody',
                  'podaj prognozę pogody']
    )
]
