import boto3
import datetime

client = boto3.client('cloudwatch')

startTime = datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
endTime = datetime.datetime.utcnow()

response = client.get_metric_statistics(
    Namespace = 'AWS/RDS',
    MetricName = 'CPUUtilization',
    Dimensions = [
        {
            'Name': 'DBInstanceIdentifier',
            'Value': 'seoul-csy-test'
        },
    ],
    StartTime = startTime,
    EndTime = endTime,
    Period = 60,
    Statistics = [ 'Maximum' ],
)

for printData in response['Datapoints']:
    print(str(printData['Timestamp']), printData['Maximum'])