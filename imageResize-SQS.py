# python 3.8
# opencv 3.8 기준의 레이어 작업이 필요합니다!

from __future__ import print_function
import os, sys
import cv2,boto3,uuid,json

s3_client = boto3.client('s3')
sqs = boto3.client('sqs')
def img_processing(file_name,download_path):
    
    src = cv2.imread(download_path, cv2.IMREAD_COLOR)
    dst = cv2.resize(src, dsize=(480, 480), interpolation=cv2.INTER_AREA)
    dst2 = cv2.resize(src, dsize=(0, 0), fx=0.4, fy=0.4, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite("/tmp/result.jpg",dst2)
    
    return "/tmp/result.jpg"
    
def lambda_handler(event, context):
    print(event)
    for record in event['Records']:
        #print(record)
        record_in = json.loads(record['body'])['Records'][0]
        #print(record_in)
        bucket = record_in['s3']['bucket']['name']
        key = record_in['s3']['object']['key']
        download_path = '/tmp/{}'.format(uuid.uuid4(), key)
    
        s3_client.download_file(bucket, key, download_path)
        file_name = key
    
        result_path = img_processing(file_name, download_path)
    
        s3_client.upload_file(result_path, bucket, 'result-img-processing/{}'.format(file_name))
    