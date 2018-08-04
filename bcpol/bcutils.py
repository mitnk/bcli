import json


def get_key_path(region_name):
    return './sessions/latest/key-{}.pem'.format(region_name)


def get_one_node_info():
    with open('./sessions/latest/deploy.json') as f:
        nodes = json.load(f)['nodes']
        for region, ins_list in nodes.items():
            return region, ins_list[0]
