import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# The base-64 encoded, encrypted key (CiphertextBlob) stored in the kmsEncryptedHookUrl environment variable
ENCRYPTED_HOOK_URL = os.environ['kmsEncryptedHookUrl']
# The Slack channel to send a message to stored in the slackChannel environment variable
SLACK_CHANNEL = os.environ['slackChannel']

HOOK_URL = "https://" + boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))['Plaintext'].decode('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(json.dumps(event))
    logger.info("Message: " + str(message))

    alarm_name = message['detail-type']
    #old_state = message['OldStateValue']
    instance_ID = message['detail']['instance-id']
    new_state = message['detail']['state']
    changed_time = message['time']

    client = boto3.client('ec2')

    response = client.describe_instances(InstanceIds=[instance_ID])

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance['Tags']:
                if(tag['Key'] == 'Name'):
                    instance_Name = tag['Value']

    slack_message = {
        'channel': SLACK_CHANNEL,
        'username': "BESPIN AWS 알리미",
        'icon_emoji': ":exclamation:",
        'text': "[알림] %s\nInstanceId : %s (%s)\nState : %s\nTime : %s" % (alarm_name, instance_ID, instance_Name, new_state, changed_time)
    }

    req = Request(HOOK_URL, json.dumps(slack_message, ensure_ascii=False).encode('utf8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)