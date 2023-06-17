import datetime
import easyocr
import numpy as np
import pyttsx3
import speech_recognition as sr
from typing import Union

import weather


WAKE = 'janko'

commands_list = {
    # TODO: Add command for turning ON/OFF radio to voice assistant
    'say_time()': [
        'która godzina',
        'jaki mamy czas',
        'która jest',
        'jaki jest czas',
    ],
    'say_current_weather()': [
        'jaka jest pogoda',
        'podaj pogodę',
        'pogoda',
    ],
    'say_daily_forecast()': [
        'jaka będzie pogoda',
        'prognoza pogody',
        'podaj prognozę pogody',
    ]
}


def speak(text: str) -> None:
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()

def get_audio() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

        try:
            said = recognizer.recognize_google(audio, language='pl-PL')
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
            return 'NOT UNDERSTOOD'
        except sr.RequestError as e:
            print('Could not request results from Google Speech Recognition service:', str(e))
            return 'ERROR'

    return said.lower()

def validate_text(text: str) -> Union[str, int]:
    match text:
        case 'NOT UNDERSTOOD':
            speak('Nie zrozumiałam.')
            return 0
        case 'ERROR':
            speak('Wystąpił błąd. Nie wiem co się dzieje.')
            return 0
        case _:
            return text

def listen() -> int:
    # TODO: Simplify this function
    text = get_audio()

    if text.count(WAKE) > 0:
        speak('Tak?')
        text = validate_text(get_audio())

        if text:
            command_to_type = ''
            commands_split = text.split(' i ')
            commands = [command for command in commands_split if len(command)]

            if len(command_to_type):
                commands.append(command_to_type)

            for command in commands:
                result = execute_command(command)

                if not result:
                    speak(f'Nie znalazłam akcji dla: {command}')

    return 1

def execute_command(text: str) -> int:
    for key, value in commands_list.items():
        for v in value:
            if v in text:
                exec(f'{key}')
                return 1

    return 0

def say_time() -> None:
    time_now = str(datetime.datetime.now().time()).split(':')
    hour = time_now[0]
    minutes = time_now[1]

    text = f'Jest godzina {hour}:{minutes}'

    speak(text)

def say_current_weather() -> None:
    speak(weather.get_current_weather_full_deccription())

def say_daily_forecast() -> None:
    speak(weather.get_daily_forecast())

def say_today_day() -> None:
    # TODO: say_today_day() function, e.g. Dzisiaj jest 4 czerwca, niedziela
    pass
