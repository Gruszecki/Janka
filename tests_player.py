import unittest

from player import Player
from settings import URLS_PATH


class PlayerTests(unittest.TestCase):
    urls_content = str()

    def setUp(self) -> None:
        with open(URLS_PATH, 'r') as f:
            self.urls_content = f.read()

    def tearDown(self) -> None:
        with open(URLS_PATH, 'w') as f:
            f.write(self.urls_content)

    def test_001_import_radio_stations(self):
        player = Player()
        self.assertGreater(len(player.radio_control.__radio_stations_list__), 1)

    def test_002_initial_station_only_when_no_stations_in_file(self):
        with open(URLS_PATH, 'w'):
            pass

        player = Player()
        self.assertEqual(len(player.radio_control.__radio_stations_list__), 1)

        player.set_next_station()
        self.assertEqual(player.get_curr_station().id, 0)

    def test_003_approach_initial_station_after_last_station(self):
        player = Player()
        num_of_stations = len(player.radio_control.__radio_stations_list__)

        if num_of_stations == 1:
            player.radio_control.add_station('Antyradio', 'https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')
            num_of_stations = len(player.radio_control.__radio_stations_list__)

        for _ in range(num_of_stations):
            player.set_next_station()

        self.assertEqual(player.get_curr_station().id, 0)

    def test_004_approach_last_station_before_initial_station(self):
        player = Player()
        num_of_stations = len(player.radio_control.__radio_stations_list__)

        if num_of_stations == 1:
            player.radio_control.add_station('Antyradio', 'https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')

        player.set_prev_station()

        self.assertNotEqual(player.get_curr_station().id, 0)

    def test_005_set_next_station(self):
        player = Player()

        if len(player.radio_control.__radio_stations_list__) == 1:
            player.radio_control.add_station('Antyradio', 'https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')

        player.set_next_station()

        self.assertGreater(int(player.get_curr_station().id), 0)

    def test_006_set_prev_station(self):
        player = Player()

        if len(player.radio_control.__radio_stations_list__) == 1:
            player.radio_control.add_station('Antyradio', 'https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')

        player.set_next_station()
        self.assertGreater(int(player.get_curr_station().id), 0)
        player.set_prev_station()
        self.assertEqual(int(player.get_curr_station().id), 0)


    def test_007_add_new_station_to_not_empty_file(self):
        player = Player()
        num_of_stations = len(player.radio_control.__radio_stations_list__)
        player.radio_control.add_station('Antyradio', 'https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')

        for _ in range(num_of_stations + 1):
            player.set_next_station()

        self.assertEqual(player.get_curr_station().id, 0)

    def test_008_add_new_station_to_empty_file(self):
        with open(URLS_PATH, 'w'):
            pass

        player = Player()
        player.radio_control.add_station('Antyradio', 'https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')

        player.set_next_station()
        self.assertEqual(player.get_curr_station().id, 1)

        player.set_next_station()
        self.assertEqual(player.get_curr_station().id, 0)

    def test_009_initial_station_when_open_file_failed(self):
        with open(URLS_PATH, 'w'):
            pass

        player = Player()
        self.assertEqual(len(player.radio_control.__radio_stations_list__), 1)

        player.set_next_station()
        self.assertEqual(player.get_curr_station().id, 0)

    def test_010_remove_station(self):
        player = Player()

        if len(player.radio_control.__radio_stations_list__) == 1:
            player.radio_control.add_station('Antyradio', 'https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')

        number_of_stations_before_remove = len(player.radio_control.__radio_stations_list__)
        last_id = max(station.id for station in player.radio_control.__radio_stations_list__)
        player.remove_station(last_id)
        number_of_stations_after_remove = len(player.radio_control.__radio_stations_list__)

        self.assertGreater(number_of_stations_before_remove, number_of_stations_after_remove)

    def test_011_set_station_by_id(self):
        player = Player()

        player.add_new_station('Testradio','https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')
        num_of_stations = len(player.radio_control.__radio_stations_list__)
        added_id = player.radio_control.__radio_stations_list__[num_of_stations - 1]

        player.set_station_by_id(added_id.id)
        current_station = player.get_curr_station()

        self.assertEqual(added_id.id, current_station.id)

    def test_012_set_station_by_name(self):
        player = Player()

        player.add_new_station('Testradio','https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')
        player.set_station_by_name('Testradio')

        current_station = player.get_curr_station()

        self.assertEqual(current_station.name.lower(), 'testradio')

    def test_013_turn_off_radio(self):
        player = Player()

        player.add_new_station('Testradio', 'https://an06.cdn.eurozet.pl/ant-web.mp3?t=1683367429522?redirected=06')

        player.set_station_by_name('Testradio')
        player.turn_off_radio()

        current_station = player.get_curr_station()

        self.assertEqual(current_station.id, 0)



if __name__ == '__main__':
    unittest.main()