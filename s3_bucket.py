# source: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html
# the code included here is taken or adapted from the Amazon S3 examples available on Boto3 documentation

# create_s3_bucket.py

import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region=None):
    try:
        s3_client = boto3.client('s3', region_name=region)

        if region and region != 'us-east-1':
            # If a region is specified and it's not us-east-1, include LocationConstraint
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        else:
            # If no region is specified, or it's us-east-1, don't include LocationConstraint
            s3_client.create_bucket(Bucket=bucket_name)

    except ClientError as e:
        print(e)

create_bucket('inventoryproj', 'us-east-1')
