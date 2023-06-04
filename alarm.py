import datetime
import logging
import time
from dataclasses import dataclass
from typing import Optional

import voice_assistant
from settings import ALARMS_PATH

logging.basicConfig(level = logging.INFO)


@dataclass
class AlarmInfo:
    id: int
    days: str

    start_h: Optional[int] = None
    start_m: Optional[int] = None
    stop_h: Optional[int] = None
    stop_m: Optional[int] = None
    station_id: Optional[int] = None
    msg: Optional[str] = None
    wake_up: Optional[bool] = False


class Alarm:
    def __init__(self):
        self.alarms = _get_alarms_from_json()

    @staticmethod
    def _get_alarms_from_json() -> None:
        # TODO: get alarms from json and put to AlarmInfo dataclass
        pass

    def start(self, player) -> None:
        while True:
            today = str(datetime.date.today().weekday() + 1)
            time_now_h = datetime.datetime.now().hour
            time_now_m = datetime.datetime.now().minute

            logging.info(f' Week day: {today}, time now: {time_now_h}:{str(time_now_m).zfill(2)}')
            for alarm in self.alarms:
                if today in alarm.days:
                    print(f'time_now: {time_now_m}, alarm.start_m: {alarm.start_m}')
                    if time_now_h == alarm.start_h and time_now_m == alarm.start_m:
                        logging.info(f' Alarm: Today is {datetime.date.today()}, time: {time_now_h}:{time_now_m}')
                        if alarm.wake_up:
                            # TODO: Set radio volume down during reading message
                            # TODO: Say what day is today
                            voice_assistant.say_current_weather()
                            voice_assistant.say_daily_forecast()
                        if alarm.msg:
                            # TODO: Set radio volume down during reading message
                            logging.info(f' Alarm message: {alarm.msg}')
                            voice_assistant.speak(f'{alarm.msg}')
                        if alarm.station_id:
                            player.set_station_by_id(alarm.station_id)
                            curr_station = player.get_curr_station()
                            logging.info(f' Alarm: Turning ON station id {alarm.station_id}, which is {curr_station["name"]}')
                    elif time_now_h == alarm.stop_h and time_now_m == alarm.stop_m:
                        logging.info(f' Alarm: Today is {datetime.date.today()}, time: {time_now_h}:{time_now_m}')
                        logging.info(f' Alarm: Turning OFF the radio')
                        player.turn_off_radio()

            time.sleep(10)

