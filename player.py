import logging
import vlc

from settings import URLS_PATH

logging.basicConfig(level = logging.INFO)


class RadioStationIterator:
    def __init__(self):
        self.curr = {'id': 0, 'name': '', 'url': ''}
        self.__parsed_stations_list__ = self.__get_urls_from_file__()

    def __get_urls_from_file__(self):
        try:
            with open(URLS_PATH) as urls:
                raw_list = [list(map(str.strip, line.split(';'))) for line in urls]

            if raw_list:
                radio_stations_list = [{'id': r_id, 'name': r_name, 'url': r_url} for r_id, r_name, r_url in raw_list]
                radio_stations_list.insert(0, {'id': 0, 'name': '', 'url': ''})
            else:
                radio_stations_list = [{'id': 0, 'name': '', 'url': ''}]
                logging.info('File with urls is empty.')

            return radio_stations_list

        except:
            logging.error('Failed to open file with urls or failed to parse raw urls to radio stations.')
            return [self.curr]


    def get_curr(self) -> dict:
        return self.curr

    def get_next(self) -> dict:
        curr_index = self.__parsed_stations_list__.index(self.curr)

        if curr_index < len(self.__parsed_stations_list__) - 1:
            self.curr = self.__parsed_stations_list__[curr_index + 1]
        else:
            self.curr = self.__parsed_stations_list__[0]

        return self.curr

    def get_prev(self) -> dict:
        curr_index = self.__parsed_stations_list__.index(self.curr)

        if curr_index:
            self.curr = self.__parsed_stations_list__[curr_index - 1]
        else:
            self.curr = self.__parsed_stations_list__[len(self.__parsed_stations_list__) - 1]

        return self.curr

    def add_station(self, name: str, url: str) -> None:
        with open(URLS_PATH, 'r+') as read_file, open(URLS_PATH, 'a') as write_file:
            read_file_list = list(read_file)
            if len(read_file_list):
                last_id = int(read_file_list[-1].split(';')[0])
                write_file.write(f'\n{last_id + 1};{name};{url}')
            else:
                write_file.write(f'1;{name};{url}')

        self.__parsed_stations_list__ = self.__get_urls_from_file__()

    def remove_station(self, id: int) -> None:
        with open(URLS_PATH, 'r') as read_file:
            read_file_list = list(read_file)

            new_stations_list = [station for station in read_file_list if str(id) != station.split(';')[0]]

        with open(URLS_PATH, 'w') as write_file:
            for station in new_stations_list:
                write_file.write(station)

        self.__parsed_stations_list__ = self.__get_urls_from_file__()


class Player:
    def __init__(self):
        self.radio_control = RadioStationIterator()
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

    def __play_next_station__(self, next_station: dict) -> None:
        if next_station['id']:
            media = self.vlc_instance.media_new(next_station['url'])
            self.media_player.set_media(media)
            self.media_player.play()
            logging.info(f' Setting station: id: {next_station["id"]}, name: {next_station["name"]}')
        else:
            self.media_player.stop()
            logging.info(' Setting station. Initial station reached. Turning off the radio...')

    def set_next_station(self):
        next_station = self.radio_control.get_next()
        self.__play_next_station__(next_station)

    def set_prev_station(self):
        next_station = self.radio_control.get_prev()
        self.__play_next_station__(next_station)

    def get_curr_station(self):
        return self.radio_control.get_curr()

    def add_new_station(self, name: str, url: str):
        self.radio_control.add_station(name, url)

    def remove_station(self, id: int):
        self.radio_control.remove_station(id)

    #TODO: Get station by id
    #TODO: Add function that turns on specific station
    #TODO: Add function that turns off radio
