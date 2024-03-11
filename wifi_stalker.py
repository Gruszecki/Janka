import time

import networks
from voice_assistant import VoiceAssistant


class WiFi_Stalker:
    def __init__(self):
        self.internet_availability = self.is_internet_available()

    def is_internet_available(self) -> bool:
        pass

    def change_network(self, name: str) -> bool:
        pass

    def stalk(self) -> str:
        pass

    def provide_internet(self):
        '''
        This method is destined to work in loop as a separate thread
        '''
        while True:
            if not self.is_internet_available():
                if self.internet_availability:
                    self.internet_availability = False
                    VoiceAssistant.speak('Utracono połączenie z internetem. ')

                name = self.stalk()

                if name:
                    self.change_network(name)

                time.sleep(1)
