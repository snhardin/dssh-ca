import config
import defaults
import logging
import os
import subprocess
import sys

def generate_host_key(name, host_dir=defaults.HOST_DIR_NAME, host_key=defaults.HOST_KEY_NAME):
    log = logging.getLogger()
    try:
        c = config.SSHConfig()
    except FileNotFoundError:
        log.error('Could not find control configuration. Did you initialize first?')
        sys.exit(1)

    full_domain = c.generate_full_hostname(name)
    complete_path = os.path.join(host_dir, full_domain)

    if os.path.exists(complete_path):
        log.error('A directory for this host already exists: %s', full_domain)
        sys.exit(1)

    try:
        os.mkdir(complete_path)
    except OSError:
        log.error('Could not create folder for new host key')
        sys.exit(1)

    try:
        subprocess.check_call(['ssh-keygen', '-t', 'ed25519', '-f', os.path.join(complete_path, 'ssh_host_ed25519_key')])
    except CalledProcessError:
        log.error('Failed to create host key')
        sys.exit(1)

    try:
        subprocess.check_call(['ssh-keygen', '-s', os.path.join(host_dir, host_key),
            '-I', name, '-h',
            '-n', name, '-n', full_domain,
            os.path.join(complete_path, 'ssh_host_ed25519_key.pub')])
    except CalledProcessError:
        log.error('Failed to sign new host key')
        sys.exit(1)

    c.host_config_stamp(complete_path, name)
    log.info('Created key for %s', full_domain)

    c.increment_host_serial_save()
    log.info('Increment host serial counter')
