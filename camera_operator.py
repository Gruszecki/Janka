import cv2
import logging
from pyzbar.pyzbar import decode

logging.basicConfig(level=logging.INFO)


def _read_network_credentials_from_qr(frame) -> tuple[str, str] | tuple[None, None]:
    data = decode(frame)
    creds = data[0].data.decode('utf-8') if data else None
    wifi_name, password = creds.split('\n') if creds else [None, None]

    return wifi_name, password


def save_picture():
    # TODO: save_picture
    pass


def get_creds_from_live_image() -> tuple[str, str] | tuple[None, None]:
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        wifi_name, password = _read_network_credentials_from_qr(frame)
        key = cv2.waitKey(1)
        if key == 27 or (wifi_name and password):  # ESC key
            logging.info(f' Camera operator: credentials read from QR code: {wifi_name} {password}')
            return wifi_name, password
