import boto3
import schedule

client = boto3.client("ec2", region_name="eu-central-1")

def create_volume_snapshots():
    volume = client.describe_volumes(
        Filters = [
            {
                "Name": "tag:Name",
                "Values": ["prod"]
            }
        ]
    )
    for volume in volume["Volumes"]:
        print(volume["VolumeId"])
        new_snapshot = client.create_snapshot(VolumeId = volume["VolumeId"])

        print(new_snapshot)

schedule.every().day.do(create_volume_snapshots)

while True:
    schedule.run_pending()