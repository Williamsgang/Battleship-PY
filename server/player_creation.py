# server/player_creation.py
# Saves the user information and encrypts it

import json
import os
import struct
import uuid
from cryptography.fernet import Fernet
from logs import logger


class PlayerCreation:
    def __init__(self, username, ip_address):
        # Logger for PlayerCreation
        self.log = logger.Logger(self.__class__.__name__)
        self.log.log_info('__init__', f'Initializing PlayerCreation for {username} with IP {ip_address}')

        # User information directory
        self.player_directory = os.path.join(os.path.dirname(__file__), 'players')
        os.makedirs(self.player_directory, exist_ok=True)

        # User information
        self.username = username
        self.ip_address = ip_address
        self.player_file = os.path.join(self.player_directory, f'{self.username}.bship')

        # Generate a key and instantiate a Fernet instance
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.log.log_info('__init__', 'Fernet key and cipher suite initialized')

    def encrypt_data(self, data: dict) -> bytes:
        self.log.log_info('encrypt_data', 'Encrypting data')
        try:
            json_data = json.dumps(data).encode('utf-8')
            encrypted_data = self.cipher_suite.encrypt(json_data)
            self.log.log_info('encrypt_data', 'Data encrypted successfully')
            return encrypted_data
        except Exception as e:
            self.log.log_error('encrypt_data', f'Error encrypting data: {e}')
            raise

    def decrypt_data(self, encrypted_data: bytes) -> dict:
        self.log.log_info('decrypt_data', 'Decrypting data')
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            self.log.log_info('decrypt_data', 'Data decrypted successfully')
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception as e:
            self.log.log_error('decrypt_data', f'Error decrypting data: {e}')
            raise

    def create_player_info(self) -> dict:
        self.log.log_info('create_player_info', 'Creating player info')
        if self.check_duplicate_user():
            self.log.log_warning('create_player_info', f'User {self.username} with IP {self.ip_address} already exists')
            raise ValueError(f"User {self.username} with IP {self.ip_address} already exists")

        try:
            player_info = {
                'name': self.username,
                'uuid': str(uuid.uuid4()),  # Generate a unique identifier for the player
                'wins': 0,
                'losses': 0,
                'destroyed_ships': 0,
                'ip_address': self.ip_address
            }
            self.log.log_info('create_player_info', f'Player info created: {player_info}')
            return player_info
        except Exception as e:
            self.log.log_error('create_player_info', f'Error creating player info: {e}')
            raise

    def save_player_info(self, player_info: dict):
        self.log.log_info('save_player_info', f'Saving player info to {self.player_file}')
        try:
            encrypted_data = self.encrypt_data(player_info)
            with open(self.player_file, 'wb') as file:
                file.write(encrypted_data)
            self.log.log_info('save_player_info', 'Player info saved successfully')
        except Exception as e:
            self.log.log_error('save_player_info', f'Error saving player info: {e}')
            raise

    def load_player_info(self) -> dict:
        self.log.log_info('load_player_info', f'Loading player info from {self.player_file}')
        try:
            with open(self.player_file, 'rb') as file:
                encrypted_data = file.read()
            player_info = self.decrypt_data(encrypted_data)
            self.log.log_info('load_player_info', 'Player info loaded successfully')
            return player_info
        except Exception as e:
            self.log.log_error('load_player_info', f'Error loading player info: {e}')
            raise

    def check_duplicate_user(self) -> bool:
        self.log.log_info('check_duplicate_user',
                          f'Checking for duplicate user {self.username} with IP {self.ip_address}')
        try:
            player_files = os.listdir(self.player_directory)
            for file in player_files:
                if file.startswith(f'{self.username}_{self.ip_address}'):
                    self.log.log_info('check_duplicate_user', f'Duplicate user found: {file}')
                    return True
            self.log.log_info('check_duplicate_user', 'No duplicate user found')
            return False
        except Exception as e:
            self.log.log_error('check_duplicate_user', f'Error checking for duplicate user: {e}')
            raise
