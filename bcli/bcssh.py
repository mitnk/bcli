import os
import bcutils


def get_ssh_cmd(region_name, ip_address):
    key_path = bcutils.get_key_path(region_name)
    return ['ssh', '-i', key_path, '-o', 'StrictHostKeyChecking no',
            'ubuntu@{}'.format(ip_address)]


def do_ssh(args):
    region_name, node_info = bcutils.get_node_info(args.node)
    if not node_info:
        print('no such node: {}'.format(args.node))
        exit(1)

    cmd = get_ssh_cmd(region_name, node_info['ipv4'])
    print(' '.join("'{}'".format(x) if ' ' in x else x for x in cmd))
    os.execvp(cmd[0], cmd)
