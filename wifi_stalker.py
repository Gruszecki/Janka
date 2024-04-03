import logging
import platform
import re
import socket
import subprocess
import time

import networks
from voice_assistant import VoiceAssistant



class WiFiStalker:
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

    def stalk(self) -> list[networks.NetworkInfo] | None:
        known_networks = list()

        for network in networks.get_networks():
            if any(network.name in available_network for available_network in self.get_available_networks()):
                known_networks.append(network)
                logging.info(f' WiFi stalker: Found password for the {network.name} network')

        return known_networks

    def connect_to_wifi(self, network: networks.NetworkInfo) -> bool:
        os_name = platform.system()

        if os_name == "Windows":
            cmd = f'netsh wlan add profile filename="{network.name}.xml" interface="Wi-Fi"'

            xml_content = f'''
                            <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                                <name>{network.name}</name>
                                <SSIDConfig>
                                    <SSID>
                                        <name>{network.name}</name>
                                    </SSID>
                                </SSIDConfig>
                                <connectionType>ESS</connectionType>
                                <connectionMode>auto</connectionMode>
                                <MSM>
                                    <security>
                                        <authEncryption>
                                            <authentication>WPA2PSK</authentication>
                                            <encryption>AES</encryption>
                                            <useOneX>false</useOneX>
                                        </authEncryption>
                                        <sharedKey>
                                            <keyType>passPhrase</keyType>
                                            <protected>false</protected>
                                            <keyMaterial>{network.password}</keyMaterial>
                                        </sharedKey>
                                    </security>
                                </MSM>
                            </WLANProfile>
                            '''

            with open(f'{network.name}.xml', 'w') as xml_file:
                xml_file.write(xml_content)

            subprocess.run(cmd, shell=True, check=True)

            cmd_connect = f'netsh wlan connect name="{network.name}" ssid="{network.name}"'
            result = subprocess.run(cmd_connect, shell=True, check=True)
            logging.info(f' WiFi Stalker: {network.name} {result}')
            return True

        elif os_name == "Linux":
            cmd = f'nmcli device wifi connect "{network.name}" password "{network.password}"'
            try:
                subprocess.run(cmd, shell=True, check=True)
                logging.info(f' WiFi Stalker: successful connection with the network: {network.name}')
                return True
            except subprocess.CalledProcessError:
                logging.info(f' WiFi Stalker: couldn\'t connect to the network: {network.name}')
                return False
        else:
            logging.info(' WiFi stalker: unsupported operating system')
            return False

    def connect_and_check_internet(self, network: networks.NetworkInfo) -> bool:
        self.connect_to_wifi(network)
        time.sleep(1)
        result = self.is_internet_available()
        return result


    def provide_internet(self) -> None:
        """
        This method is destined to work in loop as a separate thread
        """
        while True:
            if not self.is_internet_available():
                if self.internet_availability:
                    self.internet_availability = False
                    logging.info(' WiFi stalker: Internet connection lost')
                    VoiceAssistant.speak('Utraciłam połączenie z internetem. ')

                for network in self.stalk():
                    if self.connect_and_check_internet(network):
                        break

                time.sleep(1)

            else:
                if not self.internet_availability:
                    self.internet_availability = True
                    logging.info(' WiFi stalker: Internet access present')
                    VoiceAssistant.speak('Nawiązałam połączenie z internetem. ')
