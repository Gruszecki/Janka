import threading

from alarm import Alarm
from player import Player

player = Player()
alarm = Alarm()

alarm_thread = threading.Thread(target=alarm.start(player))
alarm_thread.start()

