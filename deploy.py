import datetime
import json
import logging
import os.path
import awsutils


def get_session_id():
    return datetime.datetime.now().strftime('%Y%m%d-%H%M%S')


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

    nodes_info = {}
    for region, num in configs['deploy'].get('nodes', {}).items():
        logging.info('creating {} nodes in {}'.format(num, region))
        inst_list = awsutils.create_ec2_instances(
            region, num, session_id, dir_sessions)
        nodes_info[region] = [x.instance_id for x in inst_list]
        logging.info('created: {}'.format(nodes_info[region]))

    file_deploy = os.path.join(dir_sessions, 'deploy.json')
    info = {'nodes': nodes_info}
    with open(file_deploy, 'wb') as f:
        f.write(json.dumps(info, indent=4).encode())
