# config/settings.py
# Utility functions to read settings from the settings.json file.

import json


def load_settings(file_path):
    with open(file_path, 'r') as file:
        settings = json.load(file)
    return settings


def get_client_ip(settings):
    return settings['client']['default_server_ip']


def get_client_port(settings):
    return settings['client']['port']


def get_server_host(settings):
    return settings['server']['host']


def get_server_port(settings):
    return settings['server']['port']
