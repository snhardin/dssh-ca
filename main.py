import argparse
import generate
import initialize
import logging
import sys

def get_input_args():
    """Validates and retrieves the input arguments for the program."""

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='action', help='actions that can be taken')
    subparsers.type = str.lower
    subparsers.required = True

    # Initialize command
    init_parser = subparsers.add_parser('init', help='initialize CA and metadata')
    init_parser.add_argument('domain', type=str, help='the domain to associate with host keys signed by the CA')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='generate and sign a key')
    key_type_group = gen_parser.add_mutually_exclusive_group(required=True)
    key_type_group.add_argument('--host', help='specifies a host key to generate', action='store_true')
    key_type_group.add_argument('--user', help='specifies a user key to generate', action='store_true')
    gen_parser.add_argument('-r', '--role', type=str, action='append', help='specifies role(s) to assign to a user key')
    gen_parser.add_argument('name', type=str, help='name to give to the key')

    # Revoke command
    rev_parser = subparsers.add_parser('revoke', help='revoke an existing key')

    return parser.parse_args()

def main():
    """Main method of the utility."""

    args = get_input_args()

    # Set up the logger for the program.
    log = logging.getLogger()
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s: %(message)s'))
    log.addHandler(log_handler)
    log.setLevel(logging.INFO)

    if args.action == 'generate':
        if args.host:
            if args.role is not None and len(args.role):
                log.warn('Got roles for host key, which are not used in this mode')
            generate.generate_host_key(args.name)
        elif args.user:
            generate.generate_user_key(args.name, args.role)
    elif args.action == 'init':
        initialize.initialize(
            domain=args.domain,
        )
    elif args.action == 'revoke':
        raise NotImplementedError
    else:
        raise ValueError('Unknown action specified in input')

# Allow command line utility to be run as module or in command line.
if  __name__ == '__main__':
    main()
