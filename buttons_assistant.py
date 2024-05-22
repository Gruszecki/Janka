import threading
import time

from playsound import playsound
from pynput import keyboard

import networks
from camera_operator import CameraOperator
from voice_assistant import VoiceAssistant


"""
To jest miejsce, w którym będą jedynie reakcje na naciśnięcie klawisza (wywołanie komendy z zewnątrz). 
Obsluga kamery, czytania passów do wifi leży po stronie camera operatora.
"""

class ButtonsAssistant:
    def __init__(self):
        self.camera_active = False

    def _switch_leds(self) -> None:
        # TODO
        pass

    def _make_picture(self):
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

    def _save_credentials(self):
        wifi_name, password = None, None
        camera_operator = CameraOperator()

        while self.camera_active:
            wifi_name, password = camera_operator.get_creds_from_image()

            if wifi_name == -1:
                VoiceAssistant.speak('Niepoprawny kod QR')

            if wifi_name and password:
                break

        camera_operator.close_stream()
        self.camera_active = False

        if wifi_name and password:
            networks.save_new_network(wifi_name, password)

    def _on_press(self, key):
        match key.char:
            case 'w':
                self.camera_active = not self.camera_active
                if self.camera_active:
                    get_wifi_creds_thread = threading.Thread(target=self._save_credentials)
                    get_wifi_creds_thread.start()
            case 'p':
                self._make_picture()

    def listen(self, player) -> None:
        '''
        Method destined to be looped as a separate thread.
        '''
        listener = keyboard.Listener(on_press=self._on_press)
        listener.start()

        while listener.is_alive():
            pass
