import argparse
import generate

def get_input_args():
    """Validates and retrieves the input arguments for the program."""

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='action', help='actions that can be taken')
    subparsers.type = str.lower
    subparsers.required = True

    # Initialize command
    init_parser = subparsers.add_parser('init', help='initialize CA and metadata')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='generate and sign a key')
    key_type_group = gen_parser.add_mutually_exclusive_group(required=True)
    key_type_group.add_argument('-H', '--host', help='specifies a host key to generate', action='store_true')
    key_type_group.add_argument('-u', '--user', help='specifies a user key to generate', action='store_true')
    gen_parser.add_argument('name', type=str, help='name to give to the key')

    # Revoke command
    rev_parser = subparsers.add_parser('revoke', help='revoke an existing key')

    return parser.parse_args()

def main():
    """Main method of the utility."""

    args = get_input_args()
    print(args)

    if args.action == 'generate':
        generate.hello(args.name, args.user)
    elif args.action == 'init':
        raise NotImplementedError
    elif args.action == 'revoke':
        raise NotImplementedError
    else:
        raise ValueError('Unknown action specified in input')

# Allow command line utility to be run as module or in command line.
if  __name__ == '__main__':
    main()
