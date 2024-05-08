import cv2
import logging
from pyzbar.pyzbar import decode

logging.basicConfig(level=logging.INFO)


class CameraOperator:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def close_stream(self):
        self.cap.release()

    def _read_network_credentials_from_qr(self, frame) -> tuple[str, str] | tuple[None, None]:
        data = decode(frame)
        creds = data[0].data.decode('utf-8') if data else None
        wifi_name, password = creds.split('\n') if creds else [None, None]

        return wifi_name, password

    def save_picture(self):
        # TODO: save_picture
        pass

    def get_creds_from_image(self) -> tuple[str, str] | tuple[None, None]:
        _, frame = self.cap.read()
        wifi_name, password = self._read_network_credentials_from_qr(frame)

        if wifi_name and password:
            logging.info(f' Camera operator: credentials read from QR code: {wifi_name} {password}')
            return wifi_name, password
        else:
            return None, None
