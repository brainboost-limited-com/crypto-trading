import boto3
ssh_username = "ec2-user"
ssh_key_file = "ec2/ticker.pem"

ec2 = boto3.Session(profile_name='dev', region_name='eu-west-1').client('ec2')

target_instances = ec2.describe_instances(
    Filters=[{'Name':'tag:Name','Values':['my-demo-ec2-instance']}]
)

ec2_instances = []
for each_instance in target_instances['Reservations']:
    for found_instance in each_instance['Instances']:
        ec2_instances.append(found_instance['PrivateIpAddress'])

commands = [
    "echo hi",
    "whoami",
    "hostname"
]

k = paramiko.RSAKey.from_private_key_file(ssh_key_file)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(hostname=ec2_instances[0], username=ssh_username, pkey=k, allow_agent=False, look_for_keys=False)

for command in commands:
    print("running command: {}".format(command))
    stdin , stdout, stderr = c.exec_command(command)
    print(stdout.read())
    print(stderr.read())

c.close()