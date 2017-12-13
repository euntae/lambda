import boto3
import datetime
from datetime import date
from datetime import timedelta

def lambda_handler(event, context):

    sns = boto3.client('sns')
    client = boto3.client('cloudwatch')

    dbName = 'seoul-csy-test'

    startDay = date.today() - timedelta(1)
    startTime = datetime.time(00, 00, 00)
    startDate = datetime.datetime.combine(startDay, startTime)

    endDay = date.today()
    endTime = datetime.time(00, 00, 00)
    endDate = datetime.datetime.combine(endDay, endTime)

    response = client.get_metric_statistics(
        Namespace = 'AWS/RDS',
        MetricName = 'CPUUtilization',
        Dimensions = [
            {
                'Name': 'DBInstanceIdentifier',
                'Value': dbName
            },
        ],
        StartTime = startDate,
        EndTime = endDate,
        Period = 3600,
        Statistics = [ 'Maximum' ],
    )

    result = []
    for printData in response['Datapoints']:
        result.append([str(printData['Timestamp']),printData['Maximum']])

    result.sort()

    message_body= "\n".join(map(str,result))

    response = sns.publish(
                TopicArn = 'arn:aws:sns:ap-northeast-2:449635015751:CSY-SNS-TEST',
                Subject = '[AWS알림] ' + startDay + ' RDS ' + dbName + '일일 리포트',
                Message = message_body
            )