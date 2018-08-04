import datetime
import json
import logging
import os.path
import awsutils
import bcutils
import subprocess


def ssh_to_node(region_name, ip_address):
    key_path = bcutils.get_key_path(region_name)
    cmd = ['ssh', '-i', key_path, '-o', '"StrictHostKeyChecking no"',
           'ubuntu@{}'.format(ip_address)]
    print(' '.join(cmd))


def do_ssh(args):
    try:
        region_name, node_info = bcutils.get_one_node_info()
    except (ValueError, TypeError):
        raise NotImplementedError
    ssh_to_node(region_name, node_info['ipv4'])
