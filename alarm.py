import datetime
import logging
import json
import time
from dataclasses import dataclass
from typing import Optional, Union

from settings import ALARMS_PATH
from voice_assistant import VoiceAssistant as voice_assistant

logging.basicConfig(level = logging.INFO)


@dataclass
class AlarmInfo:
    name: Optional[str] = None
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
        try:
            with open(ALARMS_PATH) as f:
                alarms_dict = json.load(f)

            alarms_list = [AlarmInfo(**alarm) for alarm in alarms_dict]

            return alarms_list
        except:
            logging.error(' Player: Failed to open file with alarms or failed to parse json alarms to dataclass.')
            return None

    def add_new_alarm(self,
                      name: Optional[str] = '',
                      start_h: Optional[int] = None,
                      start_m: Optional[int] = None,
                      stop_h: Optional[int] = None,
                      stop_m: Optional[int] = None,
                      days: Optional[str] = '1234567',
                      station_id: Optional[int] = None,
                      msg: Optional[str] = None,
                      wake_up: Optional[bool] = False) -> None:

        new_alarm = AlarmInfo(name, start_h, start_m, stop_h, stop_m, days, station_id, msg, wake_up)
        self.alarms.append(new_alarm)
        self._save_alarms_to_file()

    def _janka_to_dict(self, alarm_janka: AlarmInfo) -> dict:
        return {
            'name': alarm_janka.name,
            'start_h': alarm_janka.start_h,
            'start_m': alarm_janka.start_m,
            'stop_h': alarm_janka.stop_h,
            'stop_m': alarm_janka.stop_m,
            'days': alarm_janka.days,
            'station_id': alarm_janka.station_id,
            'msg': alarm_janka.msg,
            'wake_up': alarm_janka.wake_up
        }

    def _save_alarms_to_file(self):
        with open(ALARMS_PATH, 'w+') as f:
            alarms_dict_to_dump = [self._janka_to_dict(alarm) for alarm in self.alarms]
            alarms_json = json.dumps(alarms_dict_to_dump, indent=4, ensure_ascii=False)
            f.write(alarms_json)

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
                        if alarm.station_id:
                            player.set_station_by_id(alarm.station_id)
                            curr_station = player.get_curr_station()
                            logging.info(f' Alarm: Turning ON station id {alarm.station_id}, which is {curr_station.name}')
                        if alarm.wake_up:
                            player.set_volume(50)
                            voice_assistant.say_today_day()
                            voice_assistant.say_current_weather()
                            voice_assistant.say_daily_forecast()
                            player.set_volume(100)
                        if alarm.msg:
                            player.set_volume(50)
                            logging.info(f' Alarm message: {alarm.msg}')
                            voice_assistant.speak(f'{alarm.msg}')
                            player.set_volume(100)
                    elif time_now_h == alarm.stop_h and time_now_m == alarm.stop_m:
                        logging.info(f' Alarm: Today is {datetime.date.today()}, time: {time_now_h}:{time_now_m}')
                        logging.info(f' Alarm: Turning OFF the radio')
                        player.turn_off_radio()

            time.sleep(10)
