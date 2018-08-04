import boto3

ec2 = boto3.resource('ec2', region_name='us-west-2')

key_name = 'pcpol-test-key-001'
with open('TestKey.pem','wb') as f:
    key_pair = ec2.create_key_pair(KeyName=key_name)
    f.write(key_pair.key_material.encode('utf-8'))

ec2.create_instances(
    ImageId='ami-ba602bc2',
    InstanceType='t2.nano',
    MinCount=1,
    MaxCount=1,
    KeyName=key_name,
)

for instance in ec2.instances.all():
    print(instance, instance.tags, instance.instance_type)
