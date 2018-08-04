import logging
import bcutils
import subprocess

import bcssh


def run_cmd(node_id, cmd_single):
    region_name, info = bcutils.get_node_info(node_id)
    cmds = []
    cmd_ssh = bcssh.get_ssh_cmd(region_name, info['ipv4'])
    cmds.extend(cmd_ssh)
    cmds.append(cmd_single)
    subprocess.run(cmds)


def do_run(args):
    if not args.cmd:
        print('cmd is needed')
        exit(1)
    run_cmd(args.node, args.cmd)
