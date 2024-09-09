import boto3
from operator import itemgetter

client = boto3.client("ec2", region_name="eu-central-1")
resource = boto3.resource("ec2", region_name="eu-central-1")

instance_id = "i-0e26931d6420c25d4"

volumes = client.describe_volumes(
    Filters=[
        {
            "Name": "attachment.instance-id",
            "Values": [instance_id]
        }
    ]
)

instance_volume = volumes["Volumes"][0]
print(instance_volume)

snapshots = client.describe_snapshots(
    OwnerIds = ["self"],
    Filters = [
        {
            "Name": "volume-id",
            "Values": [instance_volume["VolumeId"]]
        }
    ]
)

latest_snapshot = sorted(snapshots["Snapshots"], key=itemgetter("StartTime"), reverse=True)[0]
print(latest_snapshot["StartTime"])

new_volume = client.create_volume(
    SnapshotId=latest_snapshot["SnapshotId"],
    AvailabilityZone="eu-central-1b",
    TagSpecifications=[
        {
            "ResourceType": "volume",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "prod"
                }
            ]
        }
    ]
)

while True:
    vol = resource.Volume(new_volume["VolumeId"])
    print(vol.state)
    if vol.state == "available":
        break

resource.Instance(instance_id).attach_volume(
    VolumeId=new_volume["VolumeId"],
    Device="/dev/xvdb"
)