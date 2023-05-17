import datetime
import logging
import time

import voice_assistant as voice

from settings import ALARMS_PATH

logging.basicConfig(level = logging.INFO)

# TODO: Change logic of storing alarms: dicts in .py instead of csv file
class Alarm:
    def __import_alarms__(self):
        try:
            with open(ALARMS_PATH, encoding='utf-8') as alarms:
                raw_list = [list(map(str.strip, alarm.split(';'))) for alarm in alarms]

            if raw_list:
                alarms_list = [
                    {
                        'id': a_id,
                        'start_h': start_h,
                        'start_m': start_m,
                        'stop_h': stop_h,
                        'stop_m': stop_m,
                        'days': days,
                        'station_id': station_id,
                        'msg': msg
                        # TODO: Add wakeup flag which indicates that it should say date (weekday), time and weather
                    }
                    for a_id, start_h, start_m, stop_h, stop_m, days, station_id, msg in raw_list
                ]

                logging.info(f'Zaimportowane alarmy: {alarms_list}')

                return alarms_list

        except:
            logging.error('Failed to open file with alarms or failed to parse raw alarms to dict.')
            return []


    def alarm(self, player):
        alarms = self.__import_alarms__()

        while True:
            today = str(datetime.date.today().weekday() + 1)
            time_now_h = str(datetime.datetime.now().hour)
            time_now_m = str(datetime.datetime.now().minute)

            logging.info(f' Week day: {today}, time now: {time_now_h}:{time_now_m}')
            for alarm in alarms:
                if today in alarm['days']:
                    if time_now_h == alarm['start_h'] and time_now_m == alarm['start_m']:
                        logging.info(f' Alarm: Today is {datetime.date.today()}, time: {time_now_h}:{time_now_m}')
                        if len(alarm['msg']):
                            logging.info(f' Alarm message: {alarm["msg"]}')
                            voice.speak(f'{alarm["msg"]}')
                        if len(alarm['station_id']):
                            player.set_station_by_id(int(alarm['station_id']))
                            curr_station = player.get_curr_station()
                            logging.info(f' Alarm: Turning ON station id {alarm["station_id"]}, which is {curr_station["name"]}')
                    elif time_now_h == alarm['stop_h'] and time_now_m == alarm['stop_m']:
                        logging.info(f' Alarm: Today is {datetime.date.today()}, time: {time_now_h}:{time_now_m}')
                        logging.info(f' Alarm: Turning OFF the radio')
                        player.turn_off_radio()

            time.sleep(10)

