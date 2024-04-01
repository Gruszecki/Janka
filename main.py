import logging
import threading
import time

import epaper
from alarm import Alarm
from player import Player
from voice_assistant import VoiceAssistant

player = Player()
alarm = Alarm()
voice_assistant = VoiceAssistant(player)


def start_threads():
    voice_assistant_thread = threading.Thread(target=voice_assistant.listen_all_the_time)
    voice_assistant_thread.start()

    epaper_thread = threading.Thread(target=epaper.run, args=(player,))
    epaper_thread.start()

    alarm_thread = threading.Thread(target=alarm.start, args=(player,))
    alarm_thread.start()

    return voice_assistant_thread, epaper_thread, alarm_thread


def watchdog():
    global voice_assistant_thread, epaper_thread, alarm_thread

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

        time.sleep(1)


voice_assistant_thread, epaper_thread, alarm_thread = start_threads()

watchdog_thread = threading.Thread(target=watchdog())
watchdog_thread.start()


# TODO: WiFi stalker
# TODO: Camera module
# TODO: AI powered voice
# TODO: Real time voice scrapping
