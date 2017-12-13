import boto3
import sys

def lambda_handler(event, context):

    sns = boto3.client('sns')
    ec2 = boto3.resource('ec2')
    filters = [{
                'Name': 'tag:CsyAuto',
                'Values': ['True']
                }, {
                'Name': 'instance-state-name',
                'Values': ['running']
                }]

    instances = ec2.instances.filter(Filters=filters)

    if len([instance.id for instance in instances]) > 0:
        instanceId = [instance.id for instance in instances]
        instanceStop = ec2.instances.filter(InstanceIds=instanceId).stop()
        print (instanceStop)
        response = sns.publish(
            TopicArn = 'arn:aws:sns:ap-northeast-2:449635015751:CSY-SNS-TEST',
            Subject = '[AWS알림] EC2 Instance 자동 종료',
            Message = str(instanceStop)
        )
    else:
        print("There is no running instances!!!")
        response = sns.publish(
            TopicArn = 'arn:aws:sns:ap-northeast-2:449635015751:CSY-SNS-TEST',
            Subject = '[실패][AWS알림] EC2 Instance 자동 종료',
            Message = 'There is no running instances!!!'
        )