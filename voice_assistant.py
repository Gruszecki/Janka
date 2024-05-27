import datetime
import logging
import time
from typing import Union

import pyttsx3
import speech_recognition as sr
from playsound import playsound

import hue
import weather
from camera_operator import CameraOperator
from voice_assistant_command_list import commands_list


logging.basicConfig(level = logging.INFO)


class VoiceAssistant:
    def __init__(self, player):
        self.player = player
        self.WAKE = 'janko'
        self.silent_mode = False

        self.speak(f'Dzień dobry. Jestem Janka.')

    # Private tools
    def _volume_gradient_asc(self, initial_volume: int = 50, target_volume: int = 100) -> None:
        for value in range(initial_volume, target_volume + 1):
            self.player.set_volume(value)
            time.sleep(0.01)

    def _volume_gradient_desc(self, initial_volume: int = 100, target_volume: int = 50) -> None:
        for value in range(initial_volume, target_volume - 1, -1):
            self.player.set_volume(value)
            time.sleep(0.01)

    def _mute(self):
        self.player.set_volume(0)

    def _get_audio(self) -> str:
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 100

        with sr.Microphone() as source:
            logging.info(' Voice assistant: listening...')
            audio = recognizer.listen(source=source, phrase_time_limit=5)
            try:
                said = recognizer.recognize_google(audio, language='pl-PL')
                logging.info(f' Voice asistant: heard: {said}')
            except sr.UnknownValueError:
                logging.debug(' Voice assistant: Google Speech Recognition could not understand audio.')
                return 'NOT UNDERSTOOD'
            except sr.RequestError as e:
                logging.error(f' Voice assistant: Could not request results from Google Speech Recognition service: {str(e)}')
                return 'ERROR'
            except Exception as e:
                logging.error(f' Voice assistant: Exception occurred: {str(e)}')
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
        if not self.silent_mode:
            text = self._get_audio()
        else:
            text = ''
            if datetime.datetime.now().hour == 6:
                self.silent_mode = False
            time.sleep(5)

        if text.count(self.WAKE) > 0:
            potential_command = text.split(self.WAKE)[-1].strip()
            potential_command_result = self._execute_command(potential_command)

            if not potential_command_result:
                self._volume_gradient_desc()
                VoiceAssistant.speak('Tak?')

                text = self._validate_text(self._get_audio())
                logging.info(f' Voice assistant: got command: {text}')
                result = self._execute_command(text) if text else None

                if text and not result:
                    VoiceAssistant.speak(f'Nie znalazłam akcji dla: {text}')

                self._volume_gradient_asc()

        return 1

    def _execute_command(self, text: str) -> int:
        for command_instance in commands_list:
            for command in command_instance.commands:
                if command in text:
                    exec(f'{command_instance.func}')
                    return 1

        return 0

    # Statics
    @staticmethod
    def speak(text: str) -> None:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        engine.setProperty('voice', 'polish')
        engine.say(text)
        engine.runAndWait()

    @staticmethod
    def dont_speak() -> None:
        engine = pyttsx3.init()
        engine.setProperty('volume', 0.0)
        engine.say('C')
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
        months = [
            'stycznia', 'lutego', 'marca', 'kwietnia',
            'maja', 'czerwca', 'lipca', 'sierpnia',
            'września', 'października', 'listopada', 'grudnia'
        ]

        weekdays = [
            'poniedziałek', 'wtorek', 'środa', 'czwartek',
            'piątek', 'sobota', 'niedziela'
        ]

        today = datetime.datetime.now()
        data_format = f'Dzisiaj jest {today.day} {months[today.month-1]}, {weekdays[today.weekday()]}'

        VoiceAssistant.speak(data_format)

    # Private methods
    def _radio_on_specific_station(self, text: str) -> bool:
        command = 'włącz radio '
        name = text[len(command):]

        if name:
            first_try_result = self.player.set_station_by_name(f'radio {name}', silent_check=True)
            if not first_try_result:
                second_try_result = self.player.set_station_by_name(name)
                if not second_try_result:
                    return False
            return True
        else:
            VoiceAssistant.speak('Nie zrozumiałam nazwy radia.')
            return False

    def _radio_off(self):
        self.player.turn_off_radio()

    def _next_station(self):
        self.player.set_next_station()

    def _prev_station(self):
        self.player.set_prev_station()

    def _take_picture(self):
        co = CameraOperator()

        VoiceAssistant.speak('Trzy')
        time.sleep(1)
        VoiceAssistant.speak('Dwa')
        time.sleep(1)

        co.take_photo()

        VoiceAssistant.speak('Jeden')
        time.sleep(1)

        co.take_photo()

        VoiceAssistant.speak('Uwaga. Robię zdjęcie. Uśmiech.')

        co.take_photo()

        playsound(r'sounds/shutter.mp3')


    @staticmethod
    def _check_lights_connection(func):
        def wrapper(args):
            passed_wo_errors = func(args)

            if not passed_wo_errors:
                VoiceAssistant.speak('Połączenie ze światłem nie powiodło się. Naciśnij przycisk na mostku i spróbuj ponownie.')

        return wrapper

    @_check_lights_connection
    def _turn_on_lights(self):
        return hue.turn_on_lights(brightness=254)

    @_check_lights_connection
    def _turn_on_soft_lights(self):
        return hue.turn_on_lights(brightness=1)

    @_check_lights_connection
    def _turn_on_mid_lights(self):
        return hue.turn_on_lights(brightness=80)

    @_check_lights_connection
    def _turn_off_lights(self):
        return hue.turn_off_lights()

    @_check_lights_connection
    def _turn_on_light_color_loop(self):
        return hue.turn_on_color_loop()

    @_check_lights_connection
    def _goodnight(self):
        self.silent_mode = True
        VoiceAssistant.speak('Dobranoc')
        self.player.turn_off_radio()
        return hue.turn_off_lights()

    def listen_all_the_time(self) -> None:
        '''
        This function listen to the voice in an infinite loop. It is meant to be called as a separate thread.
        :return: None
        '''
        while True:
            self._listen()
