import logging
import platform
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

        if system == "Windows":
            result = subprocess.check_output(["netsh", "wlan", "show", "network"])
            result = result.decode("ascii")  # konwersja bajtów na string
            result = result.replace("\r", "")
            ls = result.split("\n")
            ls = ls[4:]
            x = 0
            while x < len(ls):
                if x % 5 == 0:
                    ssids.append(ls[x])
                x += 1
        elif system == "Linux":
            result = subprocess.check_output(["nmcli", "-t", "dev", "wifi", "list"])
            result = result.decode("ascii")
            ls = result.split("\n")
            for linia in ls:
                if linia != '':
                    ssids.append(linia.split(':')[1])
        else:
            logging.info('WiFi stalker: unsupported operating system')

        return ssids

    def change_network(self, name: str) -> bool:
        pass

    def stalk(self) -> str:
        available_networks = self.get_available_networks()
        print(available_networks)



    def provide_internet(self):
        '''
        This method is destined to work in loop as a separate thread
        '''
        while True:
            if not self.is_internet_available():
                if self.internet_availability:
                    self.internet_availability = False
                    logging.info('WiFi stalker: Internet connection lost')
                    VoiceAssistant.speak('Straciłam połączenie z internetem. ')

                name = self.stalk()

                if name:
                    self.change_network(name)

                time.sleep(1)
