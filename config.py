import defaults
import json
import os

class SSHConfig:
    __data = {}
    __path = ''

    def __init__(self, control_path=defaults.CONTROL_FILE_NAME):
        if os.path.exists(control_path):
            self.__path = control_path
            with open(control_path) as file_handler:
                self.__data = json.load(file_handler)
        else:
            raise FileNotFoundError

    def __save(self):
        with open(self.__path, 'w') as file_handler:
            json.dump(self.__data, file_handler)

    def generate_full_hostname(self, name):
        return name + '.' + self.get_host_domain()

    def get_host_domain(self):
        return self.__data.get('host').get('domain')

    def host_config_stamp(self, path, name):
        full_name = name + '.' + self.get_host_domain()
        data = {
            'certificateId': name,
            'hostnames': name + ',' + full_name,
            'serial': self.__data.get('host').get('serial')
        }

        with open(os.path.join(path, defaults.DATA_FILE_NAME), 'w') as file_handler:
            json.dump(data, file_handler)

    def increment_host_serial_save(self):
        old_serial = self.__data.get('host').get('serial')
        self.__data.get('host')['serial'] = old_serial + 1
        self.__save()
