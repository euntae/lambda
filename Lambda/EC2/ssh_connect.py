import boto3
import paramiko

def ssh_handler(event, context):

    s3_client = boto3.client('s3')
    s3_client.download_file('csy-key-bucket-test', 'keys/CSY-EC2-TEST.pem', '/tmp/CSY-EC2-TEST.pem')

    ssh_key = paramiko.RSAKey.from_private_key_file('/tmp/CSY-EC2-TEST.pem')

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect( hostname = '10.33.21.191', username = 'ubuntu', pkey = ssh_key )

    stdin, stdout, stderr = ssh_client.exec_command('ps aux | head -3')

    lines = stdout.read().splitlines()
    for line in lines:
       print(line)

    print(stderr.read())

    ssh_client.close()