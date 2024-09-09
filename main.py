import boto3

ec2_client = boto3.client('ec2', region_name="eu-central-1a")
ec2_resource = boto3.resource('ec2', region_name="eu-central-1a")

reservations = ec2_client.describe_instances()
for reservation in reservations["Reservations"]:
    instances = reservation["Instances"]
    for instance in instances["Instances"]:
        print(instance["State"]["Name"])
