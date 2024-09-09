import boto3
from operator import itemgetter

client = boto3.client("ec2", region_name = "eu-central-1")

volumes = client.describe_volumes(
    Filters = [
        {
            "Name": "tag:Name",
            "Values": ["prod"]
        }
    ]
)

for volume in volumes["Volumes"]:
    snapshots = client.describe_snapshots(
        OwnerIds = ["self"],
        Filters = [
            {
                "Name": "volume-id",
                "Values": [volume["VolumeId"]]
            }
        ]
    )

    sorted_by_date = sorted(snapshots["Snapshots"], key=itemgetter("StartTime"), reverse=True)

    for snapshot in snapshots["Snapshots"]:
        print(snapshot["StartTime"])

    print("####")

    for snapshot in sorted_by_date[2:]:
        # delete snapshot
        print(snapshot["SnapshotId"])
        print(snapshot["StartTime"])

        response = client.delete_snapshot(
            SnapshotId = snapshot["SnapshotId"]
        )

        print(response)