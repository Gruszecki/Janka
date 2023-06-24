import datetime
import easyocr
import logging
import numpy as np
import pyttsx3
import speech_recognition as sr
from typing import Union

import weather


class VoiceAssistant:
    def __init__(self, player):
        self.player = player
        self.WAKE = 'janko'

        self.commands_list = {
            'self._radio_on_specific_station(text)': [
                'włącz',
            ],
            'VoiceAssistant.say_time()': [
                'która godzina',
                'jaki mamy czas',
                'która jest',
                'jaki jest czas',
            ],
            'VoiceAssistant.say_current_weather()': [
                'jaka jest pogoda',
                'podaj pogodę',
                'pogoda',
            ],
            'VoiceAssistant.say_daily_forecast()': [
                'jaka będzie pogoda',
                'prognoza pogody',
                'podaj prognozę pogody',
            ]
        }

    def _get_audio(self) -> str:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

            try:
                said = recognizer.recognize_google(audio, language='pl-PL')
            except sr.UnknownValueError:
                logging.debug(" Voice assistant: Google Speech Recognition could not understand audio.")
                return 'NOT UNDERSTOOD'
            except sr.RequestError as e:
                logging.error(' Voice assistant: Could not request results from Google Speech Recognition service:', str(e))
                return 'ERROR'

        return said.lower()

    def _validate_text(self, text: str) -> Union[str, int]:
        match text:
            case 'NOT UNDERSTOOD':
                VoiceAssistant.speak('Nie zrozumiałam.')
                return 0
            case 'ERROR':
                VoiceAssistant.speak('Wystąpił błąd. Nie wiem co się dzieje.')
                return 0
            case _:
                return text

    def _listen(self) -> int:
        text = self._get_audio()

        if text.count(self.WAKE) > 0:
            VoiceAssistant.speak('Tak?')
            text = self._validate_text(self._get_audio())
            logging.info(f' Voice assistant: got command: {text}')
            result = self._execute_command(text) if text else None

            if text and not result:
                VoiceAssistant.speak(f'Nie znalazłam akcji dla: {text}')

        return 1

    def _execute_command(self, text: str) -> int:
        for key, value in self.commands_list.items():
            for v in value:
                if v in text:
                    exec(f'{key}')
                    return 1

        return 0

    @staticmethod
    def speak(text: str) -> None:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()

    @staticmethod
    def say_time() -> None:
        time_now = str(datetime.datetime.now().time()).split(':')
        hour = time_now[0]
        minutes = time_now[1]

        text = f'Jest godzina {hour}:{minutes}'

        VoiceAssistant.speak(text)

    @staticmethod
    def say_current_weather() -> None:
        VoiceAssistant.speak(weather.get_current_weather_full_deccription())

    @staticmethod
    def say_daily_forecast() -> None:
        VoiceAssistant.speak(weather.get_daily_forecast())

    @staticmethod
    def say_today_day() -> None:
        # TODO: say_today_day() function, e.g. Dzisiaj jest 4 czerwca, niedziela
        pass

    def _radio_on_specific_station(self, text: str) -> None:
        name = text[text.find(' '):]
        self.player.set_station_by_name(name)

    def listen_all_the_time(self) -> None:
        '''
        This function listen to the voice in an infinite loop. It is meant to be called as a separate thread.
        :return: None
        '''
        while True:
            self._listen()