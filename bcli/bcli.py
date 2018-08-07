#!/usr/bin/env python
import argparse
import logging

from .deploy import do_deploy
from .ssh import do_ssh
from .info import get_info
from .run import do_run
from .terminate import do_terminate


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s][%(asctime)s] %(message)s',
    )
    logging.getLogger('botocore').setLevel(logging.WARN)
    logging.getLogger('boto3').setLevel(logging.WARN)

    parser = argparse.ArgumentParser(prog='bcli')
    subparsers = parser.add_subparsers()

    parser_sub = subparsers.add_parser('deploy',
                                       help='Deploy blockchain to EC2')
    parser_sub.add_argument('--config', '-f', type=str, default='bcli.json',
                            help='specify the config file')
    parser_sub.set_defaults(func=do_deploy)

    parser_sub = subparsers.add_parser('info', help='get states of BC')
    parser_sub.set_defaults(func=get_info)

    parser_sub = subparsers.add_parser('ssh', help='SSH to one node')
    parser_sub.add_argument('node', nargs='?', type=str, default='',
                            help='specify which node to connect')
    parser_sub.set_defaults(func=do_ssh)

    parser_sub = subparsers.add_parser('run', help='run a command')
    parser_sub.add_argument('cmd', nargs='?', type=str, default='',
                            help='run a command via ssh and exit')
    parser_sub.add_argument('--node', type=str, default='all',
                            help='specify which node to connect')
    parser_sub.set_defaults(func=do_run)

    parser_sub = subparsers.add_parser('terminate',
                                       help='terminate all AWS resources')
    parser_sub.set_defaults(func=do_terminate)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
