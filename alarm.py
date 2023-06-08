import datetime
import logging
import json
import time
from dataclasses import dataclass
from typing import Optional, Union

import voice_assistant
from settings import ALARMS_PATH

logging.basicConfig(level = logging.INFO)


@dataclass
class AlarmInfo:
    name: Optional[int] = None
    start_h: Optional[int] = None
    start_m: Optional[int] = None
    stop_h: Optional[int] = None
    stop_m: Optional[int] = None
    days: Optional[str] = '1234567'
    station_id: Optional[int] = None
    msg: Optional[str] = None
    wake_up: Optional[bool] = False


class Alarm:
    def __init__(self):
        self.alarms = self._get_alarms_from_json()

    def _get_alarms_from_json(self) -> Union[list, None]:
        alarms_list = list()

        with open(ALARMS_PATH) as f:
            alarms_dict = json.load(f)

        for alarm_name in alarms_dict:
            new_alarm = AlarmInfo()
            new_alarm.name = alarm_name
            new_alarm.start_h = alarms_dict[alarm_name]['start_h'] if alarms_dict[alarm_name]['start_h'] != -1 else None
            new_alarm.start_m = alarms_dict[alarm_name]['start_m'] if alarms_dict[alarm_name]['start_m'] != -1 else None
            new_alarm.stop_h = alarms_dict[alarm_name]['stop_h'] if alarms_dict[alarm_name]['stop_h'] != -1 else None
            new_alarm.stop_m = alarms_dict[alarm_name]['stop_m'] if alarms_dict[alarm_name]['stop_m'] != -1 else None
            new_alarm.days = alarms_dict[alarm_name]['days']
            new_alarm.station_id = alarms_dict[alarm_name]['station_id'] if alarms_dict[alarm_name]['station_id'] != -1 else None
            new_alarm.wake_up = True if alarms_dict[alarm_name]['wake_up'] else False

            alarms_list.append(new_alarm)

        return alarms_list

    def add_new_alarm(self0) -> None:
        # TODO: Add new alarm to json
        pass

    def start(self, player) -> None:
        while True:
            today = str(datetime.date.today().weekday() + 1)
            time_now_h = datetime.datetime.now().hour
            time_now_m = datetime.datetime.now().minute

            logging.info(f' Alarm: week day: {today}, time now: {time_now_h}:{str(time_now_m).zfill(2)}')
            for alarm in self.alarms:
                if today in alarm.days:
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

alarms = Alarm()