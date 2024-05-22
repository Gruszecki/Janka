import datetime
import os.path

import cv2
import logging
from pyzbar.pyzbar import decode

logging.basicConfig(level=logging.INFO)


class CameraOperator:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.read()

    def close_stream(self):
        self.cap.release()

    def _read_network_credentials_from_qr(self, frame) -> tuple[str, str] | tuple[None, None] | tuple[int, int]:
        wifi_name, password = None, None

        decoded_data = decode(frame)
        creds = decoded_data[0].data.decode('utf-8') if decoded_data else None

        if creds:
            try:
                wifi_name, password = creds.split('\n')
            except:
                logging.info(f' Camera operator: wrong QR code. Got data: {creds}')
                return -1, -1

        return wifi_name, password

    def take_photo(self):
        if not os.path.exists('photos'):
            os.mkdir('photos')

        _, frame = self.cap.read()
        cv2.imwrite(f'photos/img_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg', frame)

    def get_creds_from_image(self) -> tuple[str, str] | tuple[None, None] | tuple[int, int]:
        _, frame = self.cap.read()
        wifi_name, password = self._read_network_credentials_from_qr(frame)

        if wifi_name and password:
            logging.info(f' Camera operator: credentials read from QR code: {wifi_name} {password}')
            return wifi_name, password
        else:
            return None, None
