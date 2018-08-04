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
    for region, num in configs['deploy'].get('nodes', {}).items():
        awsutils.create_ec2_instances(region, num, session_id)
    print(configs)
