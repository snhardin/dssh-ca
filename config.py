import defaults
import json
import os

class SSHConfig:
    """Concrete implementation of configuration management."""

    __data = {}
    __path = ''

    def __init__(self, control_path=defaults.CONTROL_FILE_NAME):
        """Loads configuration into memory."""

        if os.path.exists(control_path):
            self.__path = control_path
            with open(control_path) as file_handler:
                self.__data = json.load(file_handler)
        else:
            raise FileNotFoundError

    def __save(self):
        """Saves configuration in memory to disk."""

        with open(self.__path, 'w') as file_handler:
            json.dump(self.__data, file_handler)

    def generate_full_hostname(self, name):
        """Generates a full hostname using the provided input and configuration."""

        return name + '.' + self.get_host_domain()

    def get_host_domain(self):
        """Gets the domain from configuration (host only)."""

        return self.__data.get('host').get('domain')

    def get_host_serial(self):
        """Gets the current host serial number from configuration."""

        return self.__data.get('host').get('serial')

    def get_user_serial(self):
        """Gets the current user serial number from configuration."""

        return self.__data.get('user').get('serial')

    def host_config_stamp(self, path, name):
        """Creates a file with metadata for host keys."""

        full_name = name + '.' + self.get_host_domain()
        data = {
            'certificateId': name,
            'hostnames': [name, full_name],
            'serial': self.get_host_serial()
        }

        with open(os.path.join(path, defaults.DATA_FILE_NAME), 'w') as file_handler:
            json.dump(data, file_handler)

    def increment_host_serial_save(self):
        """Increments the serial for host configuration and saves configuration to disk."""

        new_serial = self.get_host_serial() + 1
        self.__data.get('host')['serial'] = new_serial
        self.__save()

        return new_serial

    def increment_user_serial_save(self):
        """Increments the serial for user configuration and saves configuration to disk."""

        new_serial = self.get_user_serial() + 1
        self.__data.get('user')['serial'] = new_serial
        self.__save()

        return new_serial

    def user_config_stamp(self, path, username, roles):
        """Creates a file with metadata for user keys."""

        data = {
            'identity': username,
            'roles': roles,
            'serial': self.get_user_serial()
        }

        with open(os.path.join(path, defaults.DATA_FILE_NAME), 'w') as file_handler:
            json.dump(data, file_handler)
