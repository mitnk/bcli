#!/usr/bin/env python
import argparse

from deploy import do_deploy


def main(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='bcpol')
    parser.set_defaults(func=main)
    subparsers = parser.add_subparsers()

    parser_sub = subparsers.add_parser('deploy', help='Deploy blockchain to EC2')
    parser_sub.add_argument('--config', '-f', type=str, default='bcpol.json',
                            help='specify the config file')
    parser_sub.set_defaults(func=do_deploy)

    args = parser.parse_args()
    args.func(args)
