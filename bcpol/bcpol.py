#!/usr/bin/env python
import argparse
import logging

from bcdeploy import do_deploy
from bcssh import do_ssh
from bcinfo import get_info
from bcrun import do_run
from bcterminate import do_terminate


def main(args):
    pass


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s][%(asctime)s] %(message)s',
    )
    logging.getLogger('botocore').setLevel(logging.WARN)
    logging.getLogger('boto3').setLevel(logging.WARN)

    parser = argparse.ArgumentParser(prog='bcpol')
    parser.set_defaults(func=main)
    subparsers = parser.add_subparsers()

    parser_sub = subparsers.add_parser('deploy',
                                       help='Deploy blockchain to EC2')
    parser_sub.add_argument('--config', '-f', type=str, default='bcpol.json',
                            help='specify the config file')
    parser_sub.set_defaults(func=do_deploy)

    parser_sub = subparsers.add_parser('info', help='get states of BC')
    parser_sub.set_defaults(func=get_info)

    parser_sub = subparsers.add_parser('ssh', help='SSH to one node')
    parser_sub.add_argument('name', nargs='?', type=str, default='',
                            help='specify which node to connect')
    parser_sub.set_defaults(func=do_ssh)

    parser_sub = subparsers.add_parser('run', help='run a command')
    parser_sub.add_argument('cmd', nargs='?', type=str, default='',
                            help='run a command via ssh and exit')
    parser_sub.add_argument('--node', type=str, required=True,
                            help='specify which node to connect')
    parser_sub.set_defaults(func=do_run)

    parser_sub = subparsers.add_parser('terminate',
                                       help='terminate all AWS resources')
    parser_sub.set_defaults(func=do_terminate)

    args = parser.parse_args()
    args.func(args)
