import datetime
import logging
import time

import voice_assistant as voice

from alarms import alarms
from settings import ALARMS_PATH

logging.basicConfig(level = logging.INFO)

class Alarm:
    def start(self, player):
        while True:
            today = str(datetime.date.today().weekday() + 1)
            time_now_h = datetime.datetime.now().hour
            time_now_m = datetime.datetime.now().minute

            logging.info(f' Week day: {today}, time now: {time_now_h}:{time_now_m}')
            for alarm in alarms:
                if today in alarm['days']:
                    if time_now_h == alarm['start_h'] and time_now_m == alarm['start_m']:
                        logging.info(f' Alarm: Today is {datetime.date.today()}, time: {time_now_h}:{time_now_m}')
                        if alarm['wake_up']:
                            # TODO: Set radio volume down during reading message
                            # TODO: Say wake up news
                            pass
                        if len(alarm['msg']):
                            # TODO: Set radio volume down during reading message
                            logging.info(f' Alarm message: {alarm["msg"]}')
                            voice.speak(f'{alarm["msg"]}')
                        if alarm['station_id'] != -1:
                            player.set_station_by_id(alarm['station_id'])
                            curr_station = player.get_curr_station()
                            logging.info(f' Alarm: Turning ON station id {alarm["station_id"]}, which is {curr_station["name"]}')
                    elif time_now_h == alarm['stop_h'] and time_now_m == alarm['stop_m']:
                        logging.info(f' Alarm: Today is {datetime.date.today()}, time: {time_now_h}:{time_now_m}')
                        logging.info(f' Alarm: Turning OFF the radio')
                        player.turn_off_radio()

            time.sleep(10)

