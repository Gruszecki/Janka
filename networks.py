import platform

from dataclasses import dataclass

@dataclass
class NetworkInfo:
    name: str
    password: str


def _get_os() -> str:
    return platform.system()

def _json_to_dict() -> None:
    pass

def _dump_networks() -> None:
    pass

def get_networks() -> list:
    pass

def save_new_network() -> None:
    pass