import json
import logging
from dataclasses import dataclass
from settings import NETWORKS_PATH

import camera_operator


@dataclass
class NetworkInfo:
    name: str
    password: str


def get_networks() -> list:
    with open(NETWORKS_PATH, 'r') as f:
        jdata = json.load(f)

    return [NetworkInfo(name=d['name'], password=d['password']) for d in jdata]


def _dump_networks(networks) -> None:
    with open(NETWORKS_PATH, 'w+') as f:
        list_of_networks_to_dump = [{'name': network.name, 'password': network.password} for network in networks]
        data_to_dump = json.dumps(list_of_networks_to_dump, indent=4, ensure_ascii=False)
        f.write(data_to_dump)


def save_new_network() -> bool:
    wifi_name, password = camera_operator.get_creds_from_live_image()

    if not (wifi_name and password):
        return False

    networks = get_networks()

    for network in networks:
        if network.name == wifi_name:
            network.password = password
            logging.info(f' Networks: credentials updated for {wifi_name}')
            _dump_networks(networks)
            return True

    new_network = NetworkInfo(name=wifi_name, password=password)
    networks.append(new_network)
    _dump_networks(networks)
    return True
