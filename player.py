import json
import logging
import vlc
from dataclasses import dataclass
from typing import Union, Optional

from voice_assistant import VoiceAssistant as voice_assistant
from settings import URLS_PATH

logging.basicConfig(level = logging.CRITICAL)


@dataclass
class RadioStationInfo:
    id: int
    name: str
    url: str

class RadioStationIterator:
    def __init__(self):
        self.curr = RadioStationInfo(id=0, name='', url='')
        self._radio_stations_list = self.__get_urls_from_json__()

    def __get_urls_from_json__(self):
        try:
            with open(URLS_PATH, encoding='utf-8') as urls:
                urls_dict = json.load(urls)

            radio_stations_list = [RadioStationInfo(**radio_station) for radio_station in urls_dict]
            radio_stations_list.insert(0, RadioStationInfo(id=0, name='', url=''))

            return radio_stations_list

        except:
            logging.error(' Player: Failed to open file with urls or failed to parse json urls to dataclass.')
            return [self.curr]


    def get_curr(self) -> RadioStationInfo:
        return self.curr

    def get_next(self) -> RadioStationInfo:
        curr_index = self._radio_stations_list.index(self.curr)

        if curr_index < len(self._radio_stations_list) - 1:
            self.curr = self._radio_stations_list[curr_index + 1]
        else:
            self.curr = self._radio_stations_list[0]

        return self.curr

    def get_prev(self) -> RadioStationInfo:
        curr_index = self._radio_stations_list.index(self.curr)

        if curr_index:
            self.curr = self._radio_stations_list[curr_index - 1]
        else:
            self.curr = self._radio_stations_list[len(self._radio_stations_list) - 1]

        return self.curr

    def get_specific_by_id(self, id: int) -> Union[RadioStationInfo, None]:
        try:
            self.curr = [station for station in self._radio_stations_list if station.id == id][0]
        except:
            logging.critical(f' Player: There is no id {id} in imported radio stations list!')
            return None

        return self.curr

    def get_specific_by_name(self, name: str) -> Union[RadioStationInfo, None]:
        found_station = [station for station in self._radio_stations_list if station.name.lower() == name.strip().lower()]

        if len(found_station) == 1:
            self.curr = found_station[0]
            return self.curr
        elif len(found_station) == 0:
            voice_assistant.speak(f'Nie znalazłam stacji {name}')
            return None
        else:
            logging.critical(f' Player: Name {name} is ambiguous')
            return None

    def add_station(self, name: str, url: str) -> None:
        new_id = max(station.id for station in self._radio_stations_list) + 1
        new_station = RadioStationInfo(id=new_id, name=name, url=url)
        self._radio_stations_list.append(new_station)
        self._save_radio_station_list_to_file()

    def _station_to_dict(self, radio_info: RadioStationInfo) -> dict:
        return {
            'id': radio_info.id,
            'name': radio_info.name,
            'url': radio_info.url
        }

    def _save_radio_station_list_to_file(self, rs_list: Optional[list] = None):
        with open(URLS_PATH, 'w+') as f:
            if not rs_list:
                urls_dict_to_dump = [self._station_to_dict(station) for station in self._radio_stations_list]
            else:
                urls_dict_to_dump = [self._station_to_dict(station) for station in rs_list]
            urls_json = json.dumps(urls_dict_to_dump, indent=4, ensure_ascii=False)
            f.write(urls_json)

    def remove_station(self, id: int) -> None:
        try:
            with open(URLS_PATH, 'r', encoding='utf-8') as read_file:
                urls_dict = json.load(read_file)

            new_radio_stations_list = [RadioStationInfo(**radio_station) for radio_station in urls_dict if radio_station['id'] != id]
            self._save_radio_station_list_to_file(new_radio_stations_list)
            self._radio_stations_list = self.__get_urls_from_json__()
        except Exception as e:
            logging.error(f'Something went wrong during removing station: {e}')


class Player:
    def __init__(self):
        self.radio_control = RadioStationIterator()
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

    def __play_next_station__(self, next_station: RadioStationInfo) -> None:
        if next_station.id:
            media = self.vlc_instance.media_new(next_station.url)
            self.media_player.set_media(media)
            self.media_player.play()
            logging.info(f' Player: Setting station: id: {next_station.id}, name: {next_station.name}')
        else:
            self.media_player.stop()
            logging.info(' Player: Setting station. Initial station reached. Turning off the radio...')

    def set_volume(self, value: int) -> None:
        self.media_player.audio_set_volume(value)

    def set_next_station(self) -> None:
        next_station = self.radio_control.get_next()
        self.__play_next_station__(next_station)

    def set_prev_station(self) -> None:
        next_station = self.radio_control.get_prev()
        self.__play_next_station__(next_station)

    def get_curr_station(self) -> RadioStationInfo:
        return self.radio_control.get_curr()

    def set_station_by_id(self, id: int) -> None:
        next_station = self.radio_control.get_specific_by_id(id)
        if next_station:
            self.__play_next_station__(next_station)

    def set_station_by_name(self, name: str) -> None:
        next_station = self.radio_control.get_specific_by_name(name)
        if next_station:
            self.__play_next_station__(next_station)

    def turn_off_radio(self) -> None:
        next_station = self.radio_control.get_specific_by_id(0)
        self.__play_next_station__(next_station)

    def add_new_station(self, name: str, url: str) -> None:
        self.radio_control.add_station(name, url)

    def remove_station(self, id: int) -> None:
        self.radio_control.remove_station(id)
