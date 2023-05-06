import logging
import radio_settings
import vlc

logging.basicConfig(level = 0)


class RadioStationIterator:
    def __init__(self):
        self.curr = {'id': 0, 'name': '', 'url': ''}
        self.__parsed_stations_list__ = self.__get_urls_from_file__()

    def __get_urls_from_file__(self):
        try:
            with open(radio_settings.URLS_PATH) as urls:
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
        with open(radio_settings.URLS_PATH, 'r+') as read_file, open(radio_settings.URLS_PATH, 'a') as write_file:
            read_file_list = list(read_file)
            if len(read_file_list):
                last_id = int(read_file_list[-1].split(';')[0])
                write_file.write(f'\n{last_id + 1};{name};{url}')
            else:
                write_file.write(f'1;{name};{url}')

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
