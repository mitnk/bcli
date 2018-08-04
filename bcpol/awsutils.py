import os
import boto3

import constants


def create_ec2_instances(region_name, num, session_id, dir_sessions):
    ec2 = boto3.resource('ec2', region_name=region_name)
    key_file_local = os.path.join(dir_sessions, 'key-{}.pem'.format(region_name))
    key_name = 'pcpol-session-{}'.format(session_id)
    with open(key_file_local,'wb') as f:
        key_pair = ec2.create_key_pair(KeyName=key_name)
        f.write(key_pair.key_material.encode('utf-8'))
    os.chmod(key_file_local, 0o600)

    image_id = constants.IMAGES[region_name]
    inst_list = ec2.create_instances(
        ImageId=image_id,
        InstanceType='t2.nano',
        MinCount=num,
        MaxCount=num,
        KeyName=key_name,
    )
    return inst_list


def get_instance_info(region_name, instance_id):
    ec2 = boto3.resource('ec2', region_name=region_name)
    result = ec2.instances.filter(InstanceIds=[instance_id])
    infos = [x for x in result]
    return infos[0]
