import logging
import bcutils
import subprocess


def get_ssh_cmd(region_name, ip_address):
    key_path = bcutils.get_key_path(region_name)
    cmd = ['ssh', '-i', key_path, '-o', 'StrictHostKeyChecking no',
           'ubuntu@{}'.format(ip_address)]
    return cmd


def do_ssh(args):
    try:
        region_name, node_info = bcutils.get_node_info()
    except (ValueError, TypeError):
        raise NotImplementedError
    cmd = get_ssh_cmd(region_name, node_info['ipv4'])
    print(' '.join("'{}'".format(x) if ' ' in x else x for x in cmd))
