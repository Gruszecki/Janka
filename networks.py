import json
from dataclasses import dataclass
from settings import NETWORKS_PATH

@dataclass
class NetworkInfo:
    name: str
    password: str


def get_networks() -> list:
    with open(NETWORKS_PATH, 'r') as f:
        jdata = json.load(f)

    return [NetworkInfo(name=d['name'], password=d['password']) for d in jdata]


def save_new_network() -> None:
    pass