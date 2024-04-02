import logging
import platform
import re
import subprocess
import time

import networks
from voice_assistant import VoiceAssistant


class WiFi_Stalker:
    def __init__(self):
        # self.internet_availability = self.is_internet_available()
        self.internet_availability = True

    def is_internet_available(self) -> bool:
        return False

    def get_available_networks(self) -> list:
        ssids = list()
        system = platform.system()

        if system == 'Windows':
            result = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
            result = result.decode('ascii')
            result = result.replace('\r', '')
            ls = result.split('\n')
            ls = ls[4:]
            x = 0
            while x < len(ls):
                if x % 5 == 0:
                    ssids.append(ls[x])
                x += 1
        elif system == 'Linux':
            try:
                result = subprocess.check_output(['sudo', 'iwlist', 'wlan0', 'scan'])
            except subprocess.CalledProcessError as e:
                logging.error(f' WiFi stalker: Error during scanning Wi-Fi network: {e}')
                return ['']

            result = result.decode('utf-8')  # konwersja bajtów na string
            wifi_networks = re.findall(r'ESSID:"([^"]*)"', result)
            return wifi_networks
        else:
            logging.info(' WiFi stalker: unsupported operating system')

        return ssids

    def stalk(self) -> str | None:
        for network in networks.get_networks():
            if any(network.name in n.name for n in networks.get_networks()):
                logging.info(f' WiFi stalker: Found password for the {network.name} network')
                return network
            else:
                return None

    def change_network(self, name: str) -> bool:
        pass

    def provide_internet(self):
        """
        This method is destined to work in loop as a separate thread
        """
        while True:
            if not self.is_internet_available():
                if self.internet_availability:
                    self.internet_availability = False
                    logging.info(' WiFi stalker: Internet connection lost')
                    VoiceAssistant.speak('Utraciłam połączenie z internetem. ')

                network = self.stalk()

                if network:
                    self.change_network(network)

                time.sleep(1)
