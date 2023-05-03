import logging
import radio_settings
import vlc

logging.basicConfig(level = 0)


class RadioStationIterator:
    def __init__(self):
        self.curr = {'id': 0, 'name': '', 'url': ''}

        raw_urls_from_file = self.__get_urls_from_file__()
        if raw_urls_from_file:
            self.__urls_list__ = [{'id': r_id, 'name': r_name, 'url': r_url} for r_id, r_name, r_url in raw_urls_from_file]
            self.__urls_list__.insert(0, self.curr)
        else:
            self.__urls_list__ = [self.curr]
            logging.error('Failed to open or import raw urls from file.')

    def __get_urls_from_file__(self):
        try:
            with open(radio_settings.URLS_PATH) as urls:
                return [list(map(str.strip, line.split(';'))) for line in urls]
        except:
            return 0

    def get_curr(self) -> dict:
        return self.curr

    def get_next(self) -> dict:
        curr_index = self.__urls_list__.index(self.curr)

        if curr_index < len(self.__urls_list__) - 1:
            self.curr = self.__urls_list__[curr_index + 1]
        else:
            self.curr = self.__urls_list__[0]

        return self.curr

    def get_prev(self) -> dict:
        curr_index = self.__urls_list__.index(self.curr)

        if curr_index:
            self.curr = self.__urls_list__[curr_index - 1]
        else:
            self.curr = self.__urls_list__[len(self.__urls_list__) - 1]

        return self.curr


class Player:
    def __init__(self):
        self.__urls__ = RadioStationIterator()
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

    def __play_next_station__(self, next_station: dict) -> None:
        if next_station['id']:
            if 'youtube' in next_station['url'] or 'youtu.be' in next_station['url']:
                url = "qKAz9zlk6Xw"
                video = pafy.new(url)
                best = video.getbestaudio()
                media = best.url
            else:
                media = self.vlc_instance.media_new(next_station['url'])

            self.media_player.set_media(media)
            self.media_player.play()
            logging.info(f' Setting station: id: {next_station["id"]}, name: {next_station["name"]}')
        else:
            self.media_player.stop()
            logging.info(' Setting station. Initial station reached. Turning off the radio...')

    def set_next_station(self):
        next_station = self.__urls__.get_next()
        self.__play_next_station__(next_station)

    def set_prev_station(self):
        next_station = self.__urls__.get_prev()
        self.__play_next_station__(next_station)

    def get_curr_station(self):
        curr_station = self.__urls__.get_curr()
        logging.info(f' Current station: id: {curr_station["id"]}, name: {curr_station["name"]}, {curr_station["url"]}')


import time
player = Player()
player.set_next_station()
time.sleep(2)
player.set_next_station()
time.sleep(2)
player.set_next_station()
time.sleep(2)
player.set_next_station()
time.sleep(2)
player.set_prev_station()
time.sleep(2)
player.set_prev_station()
time.sleep(2)
player.get_curr_station()
time.sleep(2)

