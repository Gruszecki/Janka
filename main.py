import logging
import threading
import time

import epaper
from alarm import Alarm
from player import Player
from voice_assistant import VoiceAssistant
from wifi_stalker import WiFiStalker


player = Player()
alarm = Alarm()
voice_assistant = VoiceAssistant(player)
wifi_stalker = WiFiStalker(voice_assistant)


def start_threads():
    voice_assistant_thread = threading.Thread(target=voice_assistant.listen_all_the_time)
    voice_assistant_thread.start()

    epaper_thread = threading.Thread(target=epaper.run, args=(player,))
    epaper_thread.start()
    # epaper_thread = None

    alarm_thread = threading.Thread(target=alarm.start, args=(player,))
    alarm_thread.start()

    wifi_stalker_thread = threading.Thread(target=wifi_stalker.provide_internet)
    wifi_stalker_thread.start()

    return voice_assistant_thread, epaper_thread, alarm_thread, wifi_stalker_thread


def watchdog():
    global voice_assistant_thread, epaper_thread, alarm_thread, wifi_stalker_thread

    while True:
        if not voice_assistant_thread.is_alive():
            logging.info('Restarting voice assistant thread')
            voice_assistant_thread = threading.Thread(target=voice_assistant.listen_all_the_time)
            voice_assistant_thread.start()

        if not epaper_thread.is_alive():
            print("Restarting epaper display thread")
            epaper_thread = threading.Thread(target=epaper.run, args=(player,))
            epaper_thread.start()

        if not alarm_thread.is_alive():
            print("Restarting alarm thread")
            alarm_thread = threading.Thread(target=alarm.start, args=(player,))
            alarm_thread.start()

        if not wifi_stalker_thread.is_alive():
            print("Restarting WiFi stalker thread")
            wifi_stalker_thread = threading.Thread(target=wifi_stalker.provide_internet)
            wifi_stalker_thread.start()

        time.sleep(1)


voice_assistant_thread, epaper_thread, alarm_thread, wifi_stalker_thread = start_threads()

watchdog_thread = threading.Thread(target=watchdog())
watchdog_thread.start()


# TODO: AI powered voice
# TODO: Real time voice scrapping
