# config/settings.py
# Utility functions to read settings from the settings.json file.

import json
import os

cwd = os.path.dirname(__file__)
file_path = os.path.join(cwd, "settings.json")


def load_settings():
    with open(file_path, 'r') as file:
        settings = json.load(file)
    return settings


def get_client_ip():
    settings = load_settings()
    return settings['client']['default_server_ip']


def get_client_port():
    settings = load_settings()
    return settings['client']['port']


def get_server_host():
    settings = load_settings()
    return settings['server']['host']


def get_server_port():
    settings = load_settings()
    return settings['server']['port']
