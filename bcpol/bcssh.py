import datetime
import json
import logging
import os.path
import awsutils
import bcutils
import subprocess


def ssh_to_node(region_name, node_id):
    info = awsutils.get_instance_info(region_name, node_id)
    if info.state['Name'] != 'running':
        print('node is not ready')
        exit(0)

    key_path = bcutils.get_key_path(region_name)
    ip_address = info.public_ip_address
    cmd = ['ssh', '-i', key_path, '-o', '"StrictHostKeyChecking no"',
           'ubuntu@{}'.format(ip_address)]
    print(' '.join(cmd))


def do_ssh(args):
    try:
        region_name, node_id = bcutils.get_first_node_id()
    except (ValueError, TypeError):
        raise NotImplementedError
    ssh_to_node(region_name, node_id)
