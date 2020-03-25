import dssh_ca.config
import dssh_ca.defaults
import logging
import os
import subprocess
import sys

def generate_host_key(name, host_dir=dssh_ca.defaults.HOST_DIR_NAME, host_key=dssh_ca.defaults.HOST_KEY_NAME):
    """Generates a key for a host machine and signs it with the host CA."""

    # Set up logging and attempt to load configuration.
    log = logging.getLogger()
    try:
        c = dssh_ca.config.SSHConfig()
    except FileNotFoundError:
        log.error('Could not find control configuration. Did you initialize first?')
        sys.exit(1)

    # Check if a directory was already made with the same name.
    full_domain = c.generate_full_hostname(name)
    complete_path = os.path.join(host_dir, full_domain)

    if os.path.exists(complete_path):
        log.error('A directory for this host already exists: %s', full_domain)
        sys.exit(1)

    # Create the new folder.
    try:
        os.mkdir(complete_path)
    except OSError:
        log.error('Could not create folder for new host key')
        sys.exit(1)

    # Generate the key for the host.
    try:
        subprocess.check_call(['ssh-keygen', '-t', 'ed25519', '-f', os.path.join(complete_path, 'ssh_host_ed25519_key')])
    except subprocess.CalledProcessError:
        log.error('Failed to create host key')
        sys.exit(1)

    # Sign the key with the host CA.
    try:
        subprocess.check_call(['ssh-keygen', '-s', os.path.join(host_dir, host_key), '-I', name, '-h',
            '-n', name, '-n', full_domain, '-z', str(c.get_host_serial()), os.path.join(complete_path, 'ssh_host_ed25519_key.pub')])
    except subprocess.CalledProcessError:
        log.error('Failed to sign new host key')
        sys.exit(1)

    # Attach metadata to folder with newly-generated key.
    c.host_config_stamp(complete_path, name)
    log.info('Created key for host %s', full_domain)

    new_serial = c.increment_host_serial_save()
    log.info('Increment host serial counter to %d', new_serial)

def generate_user_key(username, roles=[], user_dir=dssh_ca.defaults.USER_DIR_NAME, user_key=dssh_ca.defaults.USER_KEY_NAME):
    """Generates a key for a user and signs it with the user CA."""

    # Set up logging and attempt to load configuration.
    log = logging.getLogger()
    try:
        c = dssh_ca.config.SSHConfig()
    except FileNotFoundError:
        log.error('Could not find control configuration. Did you initialize first?')
        sys.exit(1)

    # Check if a directory was already made with the same name.
    complete_path = os.path.join(user_dir, username)

    if os.path.exists(complete_path):
        log.error('A directory for this user already exists: %s', username)
        sys.exit(1)

    # Create the new folder.
    try:
        os.mkdir(complete_path)
    except OSError:
        log.error('Could not create folder for new user key')
        sys.exit(1)

    # Generate the key for the host.
    try:
        subprocess.check_call(['ssh-keygen', '-t', 'ed25519', '-f', os.path.join(complete_path, 'id_ed25519')])
    except subprocess.CalledProcessError:
        log.error('Failed to create user key')
        sys.exit(1)

    # Sign the key, ensuring that all roles are attached.
    args = ['ssh-keygen', '-s', os.path.join(user_dir, user_key), '-I', username, '-n', username, '-z', str(c.get_user_serial())]
    if roles is not None:
        for role in roles:
            args.append('-n')
            args.append(role)
    
    args.append(os.path.join(complete_path, 'id_ed25519.pub'))
    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError:
        log.error('Failed to sign new user key')
        sys.exit(1)

    # Attach metadata to folder with newly-generated key.
    c.user_config_stamp(complete_path, username, roles)
    log.info('Key created for user %s', username)
    
    new_serial = c.increment_user_serial_save()
    log.info('Increment user serial number to %d', new_serial)
