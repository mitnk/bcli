import time
import datetime
import json
import logging
import os.path
import awsutils

from collections import defaultdict


def get_session_id():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def do_deploy(args):
    if not os.path.exists(args.config):
        print('no such file: {}'.format(args.config))
        exit(1)

    with open(args.config) as f:
        configs = json.load(f)
    if 'deploy' not in configs:
        print('deploy not found in configs')
        exit(1)

    session_id = get_session_id()

    dir_sessions = './sessions/{}'.format(session_id)
    if not os.path.exists(dir_sessions):
        os.makedirs(dir_sessions, exist_ok=True)
    symlink_latest = os.path.abspath('./sessions/latest')
    if os.path.lexists(symlink_latest):
        os.remove(symlink_latest)
    os.symlink(
        os.path.abspath(dir_sessions),
        symlink_latest,
        target_is_directory=True,
    )

    instance_list = []
    nodes_info = defaultdict(list)
    for region_name, num in configs['deploy'].get('nodes', {}).items():
        logging.info('creating {} nodes in {}'.format(num, region_name))
        node_id_list = awsutils.create_ec2_instances(
            region_name, num, session_id, dir_sessions)
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
            info = awsutils.get_instance_info(region_name, node_id)
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
                    'image_id': info.image_id,
                    'tags': info.tags,
                })
        if len(_states_ok) == len(instance_list):
            break
        time.sleep(10.0)
    logging.info('all instances are ready now')

    # assign a new scurity group to the instances
    for region_name in instance_info:
        sg = awsutils.create_security_group(region_name, session_id, ip_list)
        for instance in instance_info[region_name]:
            logging.info('assign new SG to instance: {}'.format(instance))
            sg_list = [x['GroupId'] for x in instance.security_groups]
            sg_list.append(sg.id)
            instance.modify_attribute(Groups=sg_list)

    file_deploy = os.path.join(dir_sessions, 'deploy.json')
    info = {'nodes': nodes_info}
    with open(file_deploy, 'wb') as f:
        f.write(json.dumps(info, indent=4).encode())
