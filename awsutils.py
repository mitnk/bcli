import boto3

def create_ec2_instances(region_name, num, session_id):
    ec2 = boto3.resource('ec2', region_name=region_name)
    for i in range(num):
        key_name = 'pcpol-session-{}'.format(session_id)
        key_name_local = 'pcpol-key-{}-{}'.format(region_name, i)
        with open('{}.pem'.format(key_name_local),'wb') as f:
            key_pair = ec2.create_key_pair(KeyName=key_name)
            f.write(key_pair.key_material.encode('utf-8'))

        ins = ec2.create_instances(
            ImageId='ami-ba602bc2',
            InstanceType='t2.nano',
            MinCount=1,
            MaxCount=1,
            KeyName=key_name,
        )
        import pdb; pdb.set_trace()

    #for instance in ec2.instances.all():
    #    print(instance, instance.tags, instance.instance_type)
