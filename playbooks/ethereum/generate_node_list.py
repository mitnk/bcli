import re
import glob
import json
import os


def get_enode_info():
    result = []
    prefix = '/tmp/ansible-eth-node-info-'
    for file_name in glob.glob('{}*'.format(prefix)):
        node_id = file_name.replace(prefix, '')
        with open(file_name) as f:
            content = f.read().replace('\n', '')
            enode_id = re.search(r'enode://([0-9a-f]{40,})@', content).group(1)
        result.append({'node_id': node_id, 'enode_id': enode_id})
        os.remove(file_name)
    return result


def get_ip_address():
    result = {}
    with open(os.path.expanduser('~/.bcli/sessions/latest/deploy.json')) as f:
        nodes = json.load(f)['nodes']
        for node_list in nodes.values():
            for item in node_list:
                result[item['id']] = item['ipv4']
    return result


def main():
    ip_mapping = get_ip_address()
    node_list = get_enode_info()
    with open('/tmp/add-peers.sh', 'w') as f:
        f.write('cd\n')
        for item in node_list:
            ipv4 = ip_mapping[item['node_id']]
            enode_id = item['enode_id']
            uri = 'enode://{}@{}:30303'.format(enode_id, ipv4)
            cmd = "geth attach ipc:gethDataDir/geth.ipc --exec 'admin.addPeer(\"{}\")'".format(uri)
            f.write('{}\n'.format(cmd))


if __name__ == '__main__':
    main()
