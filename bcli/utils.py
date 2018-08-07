import datetime
import json
import os.path

from bcli import constants


def generate_session_id():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def create_dir_session(session_id):
    dir_session = os.path.expanduser('~/.bcli/sessions/{}'.format(session_id))
    os.makedirs(dir_session, exist_ok=True)
    symlink_latest = os.path.expanduser('~/.bcli/sessions/latest')
    if os.path.lexists(symlink_latest):
        os.remove(symlink_latest)
    os.symlink(dir_session, symlink_latest, target_is_directory=True)
    return dir_session


def get_dir_session():
    return os.path.expanduser('~/.bcli/sessions/latest')


def get_session_id():
    dir_session = get_dir_session()
    with open(os.path.join(dir_session, 'deploy.json')) as f:
        return json.load(f)['session_id']


def get_key_path(region_name):
    dir_session = get_dir_session()
    return os.path.join(dir_session, 'key-{}.pem'.format(region_name))


def get_node_info(node_id=None):
    dir_session = get_dir_session()
    with open(os.path.join(dir_session, 'deploy.json')) as f:
        nodes = json.load(f)['nodes']
        for region, ins_list in nodes.items():
            for item in ins_list:
                if not node_id:
                    return region, ins_list[0]
                if item['id'] == node_id:
                    return region, item
    return None, None


def get_all_nodes_info():
    dir_session = get_dir_session()
    with open(os.path.join(dir_session, 'deploy.json')) as f:
        return json.load(f)['nodes']


def get_key_pair_name(session_id=None):
    if not session_id:
        session_id = get_session_id()
    return '{}{}'.format(constants.KEYPAIR_PREFIX, session_id)


def get_security_group_name(session_id=None):
    if not session_id:
        session_id = get_session_id()
    return '{}{}'.format(constants.SG_PREFIX, session_id)


def get_deployed_info_file():
    dir_session = get_dir_session()
    return os.path.join(dir_session, 'deploy.json')


def no_sessions():
    file_deployed_info = get_deployed_info_file()
    return not os.path.exists(file_deployed_info)
