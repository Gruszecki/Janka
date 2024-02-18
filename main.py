import threading

from alarm import Alarm
from player import Player
from voice_assistant import VoiceAssistant

import epaper


player = Player()
alarm = Alarm()
voice_assistant = VoiceAssistant(player)

voice_assistant_thread = threading.Thread(target=voice_assistant.listen_all_the_time)
voice_assistant_thread.start()

alarm_thread = threading.Thread(target=alarm.start(player))
alarm_thread.start()

epaper_thread = threading.Thread(target=epaper.run)
epaper_thread.start()
