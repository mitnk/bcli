import logging
import os
import subprocess

from bcli import ssh
from bcli import utils


def run_cmd(node_id, cmd_single):
    info_list = []
    if node_id == 'all':
        nodes_info = utils.get_all_nodes_info()
        for region_name in nodes_info:
            for info in nodes_info[region_name]:
                info_list.append((region_name, info))
    else:
        region_name, info = utils.get_node_info(node_id)
        info_list = [(region_name, info)]
    for region_name, info in info_list:
        cmds = []
        cmd_ssh = ssh.get_ssh_cmd(region_name, info['ipv4'])
        cmds.extend(cmd_ssh)
        cmds.append(cmd_single)
        logging.info('run cmd on {} ...'.format(info['id']))
        subprocess.run(cmds)


def do_run(args):
    if not args.cmd:
        print('cmd is needed')
        exit(1)

    file_deployed_info = utils.get_deployed_info_file()
    if not os.path.exists(file_deployed_info):
        print('deployed info file not found')
        exit(1)

    run_cmd(args.node, args.cmd)
