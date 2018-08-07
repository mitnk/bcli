import os
import boto3

from bcli import constants


def create_ec2_instances(region_name, num, key_name, dir_keys):
    ec2 = boto3.resource('ec2', region_name=region_name)
    key_file_local = os.path.join(dir_keys, 'key-{}.pem'.format(region_name))
    with open(key_file_local, 'wb') as f:
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


def get_instances_info(region_name, instance_ids):
    if not isinstance(instance_ids, list):
        instance_ids = [instance_ids]
    ec2 = boto3.resource('ec2', region_name=region_name)
    result = ec2.instances.filter(InstanceIds=instance_ids)
    return [x for x in result]


def create_security_group(region_name, sg_name, ip_list):
    """
    1. fetch IP Address list for all nodes
    2. create a SG to let these nodes can access each other
    """
    ec2 = boto3.resource('ec2', region_name=region_name)
    sec_group = ec2.create_security_group(
        GroupName=sg_name, Description='blockcain SG')
    for ipv4 in ip_list:
        sec_group.authorize_ingress(
            CidrIp='{}/32'.format(ipv4),
            IpProtocol='-1',
            FromPort=-1,
            ToPort=-1
        )
    return sec_group


def delete_security_groups(region_name, sg_id_list):
    ec2 = boto3.client('ec2', region_name=region_name)
    for sg_id in sg_id_list:
        ec2.delete_security_group(GroupId=sg_id)


def get_key_pairs(region_name, key_name_list):
    ec2 = boto3.client('ec2', region_name=region_name)
    return ec2.describe_key_pairs(KeyNames=key_name_list)


def delete_key_pair(region_name, key_name):
    ec2 = boto3.client('ec2', region_name=region_name)
    ec2.delete_key_pair(KeyName=key_name)
