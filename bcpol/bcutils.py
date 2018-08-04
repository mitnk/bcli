import json

import constants


def get_key_path(region_name):
    return './sessions/latest/key-{}.pem'.format(region_name)


def get_node_info(node_id=None):
    with open('./sessions/latest/deploy.json') as f:
        nodes = json.load(f)['nodes']
        for region, ins_list in nodes.items():
            for item in ins_list:
                if node_id is None:
                    return region, ins_list[0]
                if item['id'] == node_id:
                    return region, item
    return None, None


def get_all_nodes_info():
    with open('./sessions/latest/deploy.json') as f:
        return json.load(f)['nodes']


def get_session_id():
    with open('./sessions/latest/deploy.json') as f:
        return json.load(f)['session_id']


def get_security_group_name(session_id=None):
    if not session_id:
        session_id = get_session_id()
    return '{}{}'.format(constants.SG_PREFIX, session_id)
