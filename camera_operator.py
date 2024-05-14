import datetime
import os.path
import time

import cv2
import logging
from pyzbar.pyzbar import decode

from voice_assistant import VoiceAssistant

logging.basicConfig(level=logging.INFO)


class CameraOperator:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def close_stream(self):
        self.cap.release()

    def _read_network_credentials_from_qr(self, frame) -> tuple[str, str] | tuple[None, None]:
        wifi_name, password = None, None

        decoded_data = decode(frame)
        creds = decoded_data[0].data.decode('utf-8') if decoded_data else None

        if creds:
            try:
                wifi_name, password = creds.split('\n')
            except:
                logging.info(f' Camera operator: wrong QR code. Got data: {creds}')
                VoiceAssistant.speak('Niepoprawny kod QR')

        return wifi_name, password

    def take_photo(self):
        if not os.path.exists('photos'):
            os.mkdir('photos')

        VoiceAssistant.speak('Trzy')
        time.sleep(1)
        VoiceAssistant.speak('Dwa')
        time.sleep(1)

        _, frame = self.cap.read()
        cv2.imwrite(f'photos/img_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg', frame)

        VoiceAssistant.speak('Jeden')
        time.sleep(1)

        _, frame = self.cap.read()
        cv2.imwrite(f'photos/img_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg', frame)

        VoiceAssistant.speak('Uwaga. Robię zdjęcie. Uśmiech.')

        _, frame = self.cap.read()
        cv2.imwrite(f'photos/img_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg', frame)

        # TODO: play camera sound


    def get_creds_from_image(self) -> tuple[str, str] | tuple[None, None]:
        _, frame = self.cap.read()
        wifi_name, password = self._read_network_credentials_from_qr(frame)

        if wifi_name and password:
            logging.info(f' Camera operator: credentials read from QR code: {wifi_name} {password}')
            return wifi_name, password
        else:
            return None, None
