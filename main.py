import threading

from alarm import Alarm
from player import Player

# TODO: Add voice assistant to main

player = Player()
alarm = Alarm()

alarm_thread = threading.Thread(target=alarm.start(player))
alarm_thread.start()

