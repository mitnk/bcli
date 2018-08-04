import json


def get_key_path(region_name):
    return './sessions/latest/key-{}.pem'.format(region_name)


def get_one_node_info():
    with open('./sessions/latest/deploy.json') as f:
        nodes = json.load(f)['nodes']
        for region, ins_list in nodes.items():
            return region, ins_list[0]


def get_all_nodes_info():
    with open('./sessions/latest/deploy.json') as f:
        return json.load(f)['nodes']


def get_session_id():
    with open('./sessions/latest/deploy.json') as f:
        return json.load(f)['session_id']


def get_security_group_name(session_id=None):
    if not session_id:
        session_id = get_session_id()
    return 'bcpol-{}'.format(session_id)
