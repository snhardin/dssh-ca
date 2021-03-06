import dssh_ca.defaults
import json
import logging
import os
import subprocess
import sys

def initialize(
    domain,
    control_name=dssh_ca.defaults.CONTROL_FILE_NAME,
    host_dir=dssh_ca.defaults.HOST_DIR_NAME,
    host_key=dssh_ca.defaults.HOST_KEY_NAME,
    user_dir=dssh_ca.defaults.USER_DIR_NAME,
    user_key=dssh_ca.defaults.USER_KEY_NAME
):
    """Initializes configuration."""

    log = logging.getLogger()

    # Check for existing config file
    if os.path.exists(control_name):
        log.error('SSH CA already initialized here: ' + control_name + ' file exists')
        sys.exit(1)
        return

    data = {
        'host': {
            'serial': 1,
            'domain': domain,
        },
        'user': {
            'serial': 1,
        },
    }

    try:
        os.mkdir(host_dir)
        os.mkdir(user_dir)
    except OSError:
        log.error('Failed to create user and host directories')
        sys.exit(1)

    try:
        subprocess.check_call(['ssh-keygen', '-t', 'ed25519', '-f', os.path.join(user_dir, user_key)])
    except subprocess.CalledProcessError:
        log.error('Failed to create user CA key')
        sys.exit(1)

    try:
        subprocess.check_call(['ssh-keygen', '-t', 'ed25519', '-f', os.path.join(host_dir, host_key)])
    except subprocess.CalledProcessError:
        log.error('Failed to create host CA key')
        sys.exit(1)

    with open(control_name, 'w') as file_handler:
        json.dump(data, file_handler)

    log.info('Initialized new CA repo successfully')
