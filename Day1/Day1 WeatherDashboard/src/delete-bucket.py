import boto3
import os
from botocore.exceptions import ClientError

# Load environment variables
# Make sure to set your AWS credentials and region
bucket_name = 'weather-dashboard-cd'  # Replace with your bucket name

def delete_all_objects(bucket):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    
    # Delete all objects in the bucket
    bucket.objects.all().delete()
    print(f"All objects deleted from bucket: {bucket_name}")

def delete_bucket(bucket):
    s3 = boto3.client('s3')
    
    # Delete the bucket
    try:
        s3.delete_bucket(Bucket=bucket)
        print(f"Bucket {bucket} deleted successfully.")
    except ClientError as e:
        print(f"Error deleting bucket: {e}")

def main():
    delete_all_objects(bucket_name)
    delete_bucket(bucket_name)

if __name__ == '__main__':
    main()