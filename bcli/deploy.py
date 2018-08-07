import json
import logging
import os.path
import time

from collections import defaultdict

from bcli import awsutils
from bcli import utils


def generate_ansible_inventory_file(dir_session, nodes_info):
    file_inv = os.path.join(dir_session, "ansible.ini")
    with open(file_inv, 'w') as f:
        for region_name in nodes_info:
            key_file = utils.get_key_path(region_name)
            f.write('[{}]\n'.format(region_name))
            for item in nodes_info[region_name]:
                f.write('{}  '.format(item['id']))
                f.write('ansible_host={}  '.format(item['ipv4']))
                f.write('ansible_user=ubuntu  ')
                f.write('ansible_ssh_private_key_file={}\n'.format(key_file))
            f.write('\n')


def do_deploy(args):
    if not os.path.exists(args.config):
        print('no such file: {}'.format(args.config))
        exit(1)

    with open(args.config) as f:
        configs = json.load(f)
    if 'deploy' not in configs:
        print('deploy not found in configs')
        exit(1)

    session_id = utils.generate_session_id()
    dir_session = utils.create_dir_session(session_id)

    instance_list = []
    nodes_info = defaultdict(list)
    key_name = utils.get_key_pair_name(session_id)
    for region_name, num in configs['deploy'].get('nodes', {}).items():
        logging.info('creating {} nodes in {}'.format(num, region_name))
        node_id_list = awsutils.create_ec2_instances(
            region_name, num, key_name, dir_session)
        node_id_list = [x.instance_id for x in node_id_list]
        logging.info('created: {}'.format(node_id_list))
        for x in node_id_list:
            instance_list.append((region_name, x))

    logging.info('checking state of instances ...')
    _states_ok = {}
    ip_list = set()
    instance_info = defaultdict(list)
    while 1:
        for region_name, node_id in instance_list:
            info = awsutils.get_instances_info(region_name, node_id)[0]
            _key = (region_name, node_id)
            if _key not in _states_ok and info.state['Name'] == 'running':
                _states_ok[_key] = True
                ip_list.add(info.public_ip_address)
                logging.info('instance {} is ready'.format(_key))
                instance_info[region_name].append(info)
                nodes_info[region_name].append({
                    'id': info.id,
                    'type': info.instance_type,
                    'ipv4': info.public_ip_address,
                    'tags': info.tags,
                })
        if len(_states_ok) == len(instance_list):
            break
        time.sleep(10.0)
    logging.info('all instances are ready now')

    # assign a new scurity group to the instances
    sg_name = utils.get_security_group_name(session_id)
    for region_name in instance_info:
        sg = awsutils.create_security_group(region_name, sg_name, ip_list)
        for instance in instance_info[region_name]:
            logging.info('assign new SG to instance: {}'.format(instance.id))
            sg_list = [x['GroupId'] for x in instance.security_groups]
            sg_list.append(sg.id)
            instance.modify_attribute(Groups=sg_list)

    file_deploy = os.path.join(dir_session, 'deploy.json')
    info = {
        'session_id': session_id,
        'nodes': nodes_info,
    }
    with open(file_deploy, 'wb') as f:
        f.write(json.dumps(info, indent=4).encode())

    generate_ansible_inventory_file(dir_session, nodes_info)
