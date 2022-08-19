import json
import boto3
from datetime import datetime
import requests
import os

print('Loading function')

s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id = os.getenv('ACCESS_KEY_ID'), aws_secret_access_key = os.getenv('SECRET_ACCESS_KEY_ID'))


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    s3info = event['Records'][0]['s3']
    bucket = s3info['bucket']['name']
    key = s3info['object']['key']
    response = s3.head_object(Bucket=bucket, Key=key)
    custom_labels = response['Metadata']['customlabels']
    labels = []
    if (custom_labels != ""):
        cl_list = custom_labels.split(",")
        for l in cl_list:
            labels.append(l.strip())
    client = boto3.client('rekognition')
    s3object = {'S3Object':{'Bucket':bucket,'Name':key}}
    response = client.detect_labels(Image=s3object)
    timestamp = datetime.now().strftime('%Y-%d-%mT%H:%M:%S')
    for i in range(len(response['Labels'])):
        labels.append(response['Labels'][i]['Name'])
    url = "https://search-photos-z5ptjwic2ktfmrk6vmd3lpz52y.us-east-1.es.amazonaws.com/photos/_doc/"
    payload = {"objectKey": key, "bucket": bucket, "createdTimestamp": timestamp, "labels": labels}
    print(payload)
    r = requests.post(url, auth=("Meri", "Gjs920568#"), json=payload)
    return("yep")