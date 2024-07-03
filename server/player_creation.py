# server/player_creation.py
# Saves the user information and encrypts it

import json
import os
import struct
import uuid
from cryptography.fernet import Fernet
from logs import logger


class PlayerCreation:
    def __init__(self, username):
        self.log = logger.Logger(self.__class__.__name__)
        self.log.log_info('__init__', f'Initializing PlayerCreation for {username}')
        player_directory = os.path.join(os.path.dirname(__file__), 'players')
        os.makedirs(player_directory, exist_ok=True)
        self.username = username
        self.player_file = os.path.join(player_directory, f'{self.username}.bship')

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
        try:
            player_info = {
                'name': self.username,
                'uuid': str(uuid.uuid4()),  # Generate a unique identifier for the player
                'wins': 0,
                'losses': 0,
                'destroyed_ships': 0
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

    def serialize_player_info(self, player_info: dict) -> bytes:
        self.log.log_info('serialize_player_info', 'Serializing player info')
        try:
            username = player_info['name'].encode('utf-8')
            uuid_str = player_info['uuid'].encode('utf-8')
            wins = player_info['wins']
            losses = player_info['losses']
            destroyed_ships = player_info['destroyed_ships']

            serialized_data = struct.pack(f'!I{len(username)}sI{len(uuid_str)}sIII', len(username), username, len(uuid_str), uuid_str,
                                          wins, losses, destroyed_ships)
            self.log.log_info('serialize_player_info', 'Player info serialized successfully')
            return serialized_data
        except Exception as e:
            self.log.log_error('serialize_player_info', f'Error serializing player info: {e}')
            raise

    def deserialize_player_info(self, data: bytes) -> dict:
        self.log.log_info('deserialize_player_info', 'Deserializing player info')
        try:
            username_length = struct.unpack('!I', data[:4])[0]
            offset = 4 + username_length
            username = data[4:offset].decode('utf-8')
            uuid_length = struct.unpack('!I', data[offset:offset + 4])[0]
            offset += 4
            uuid_str = data[offset:offset + uuid_length].decode('utf-8')
            offset += uuid_length
            wins, losses, destroyed_ships = struct.unpack('!III', data[offset:offset + 12])

            player_info = {'name': username, 'uuid': uuid_str, 'wins': wins, 'losses': losses, 'destroyed_ships': destroyed_ships}
            self.log.log_info('deserialize_player_info', 'Player info deserialized successfully')
            return player_info
        except Exception as e:
            self.log.log_error('deserialize_player_info', f'Error deserializing player info: {e}')
            raise

    def encrypt_binary_data(self, data: bytes) -> bytes:
        self.log.log_info('encrypt_binary_data', 'Encrypting binary data')
        try:
            encrypted_data = self.cipher_suite.encrypt(data)
            self.log.log_info('encrypt_binary_data', 'Binary data encrypted successfully')
            return encrypted_data
        except Exception as e:
            self.log.log_error('encrypt_binary_data', f'Error encrypting binary data: {e}')
            raise

    def decrypt_binary_data(self, encrypted_data: bytes) -> bytes:
        self.log.log_info('decrypt_binary_data', 'Decrypting binary data')
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            self.log.log_info('decrypt_binary_data', 'Binary data decrypted successfully')
            return decrypted_data
        except Exception as e:
            self.log.log_error('decrypt_binary_data', f'Error decrypting binary data: {e}')
            raise

    def save_player_info_binary(self, player_info: dict):
        self.log.log_info('save_player_info_binary', f'Saving player info to {self.player_file} in binary format')
        try:
            serialized_data = self.serialize_player_info(player_info)
            encrypted_data = self.encrypt_binary_data(serialized_data)
            with open(self.player_file, 'wb') as file:
                file.write(encrypted_data)
            self.log.log_info('save_player_info_binary', 'Player info saved successfully in binary format')
        except Exception as e:
            self.log.log_error('save_player_info_binary', f'Error saving player info in binary format: {e}')
            raise

    def load_player_info_binary(self) -> dict:
        self.log.log_info('load_player_info_binary', f'Loading player info from {self.player_file} in binary format')
        try:
            with open(self.player_file, 'rb') as file:
                encrypted_data = file.read()
            serialized_data = self.decrypt_binary_data(encrypted_data)
            player_info = self.deserialize_player_info(serialized_data)
            self.log.log_info('load_player_info_binary', 'Player info loaded successfully in binary format')
            return player_info
        except Exception as e:
            self.log.log_error('load_player_info_binary', f'Error loading player info in binary format: {e}')
            raise


# Example usage
if __name__ == "__main__":
    username = "Player1"
    player_creator = PlayerCreation(username)
    player_info = player_creator.create_player_info()
    player_creator.save_player_info(player_info)
    loaded_player_info = player_creator.load_player_info()
    print(loaded_player_info)

    player_creator.save_player_info_binary(player_info)
    loaded_player_info_binary = player_creator.load_player_info_binary()
    print(loaded_player_info_binary)
