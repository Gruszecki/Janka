import logging
import platform
import re
import socket
import subprocess
import time

import networks
from voice_assistant import VoiceAssistant


class WiFi_Stalker:
    def __init__(self):
        self.internet_availability = self.is_internet_available()

    def is_internet_available(self) -> bool:
        try:
            socket.create_connection(('www.google.com', 80), timeout=10)
            return True
        except OSError:
            pass

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

            result = result.decode('utf-8')
            wifi_networks = re.findall(r'ESSID:"([^"]*)"', result)
            return wifi_networks
        else:
            logging.info(' WiFi stalker: unsupported operating system')

        return ssids

    def stalk(self) -> networks.NetworkInfo | None:
        for network in networks.get_networks():
            if any(network.name in n.name for n in networks.get_networks()):
                logging.info(f' WiFi stalker: Found password for the {network.name} network')
                # TODO: Check if that network has internet access
                return network
            else:
                return None

    def change_network(self, name: networks.NetworkInfo) -> bool:
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

            else:
                if not self.internet_availability:
                    self.internet_availability = True
                    logging.info(' WiFi stalker: Internet access present')
                    VoiceAssistant.speak('Połączenie z internetem zostało nawiązane. ')
