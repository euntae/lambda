import boto3
import json

global_resource = boto3.client('ec2')
regions = global_resource.describe_regions()

for region in regions["Regions"]:
    client = boto3.client('ec2', region_name=region["RegionName"])
    result = []
    response = client.describe_instances()

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if 'Tags' in instance:
                if 'bespinAuto' not in [tag["Key"] for tag in instance["Tags"]]:
                    print(region["RegionName"], instance["InstanceId"])
                    result.append(instance["InstanceId"])
            else:
                print(region["RegionName"], instance["InstanceId"], "NOT TAGGED")
                result.append(instance["InstanceId"])

    if result:
        tag_response = client.create_tags(
                        Resources=result,
                        Tags=[
                                {
                                    'Key':'bespinAuto',
                                    'Value':'True'
                                }
                            ])