import threading

from pynput import keyboard

import networks
from camera_operator import CameraOperator


"""
To jest miejsce, w którym będą jedynie reakcje na naciśnięcie klawisza (wywołanie komendy z zewnątrz). 
Obsluga kamery, czytania passów do wifi leży po stronie camera operatora.
"""

class ButtonsAssistant:
    def __init__(self):
        self.camera_operator = None
        self.camera_active = False

    def _switch_leds(self) -> None:
        # TODO
        pass

    def _make_picture(self):
        camera_operator = CameraOperator()
        camera_operator.take_photo()

    def _save_credentials(self):
        wifi_name, password = None, None
        self.camera_operator = CameraOperator()

        while self.camera_active:
            wifi_name, password = self.camera_operator.get_creds_from_image()

            if wifi_name and password:
                break

        self.camera_operator.close_stream()
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
