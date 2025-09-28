import os
import boto3
from dotenv import load_dotenv
from main.utils.time_utils import get_time_msk

load_dotenv()

# Данные для подключения к стандартному хранилищу
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
REGION_NAME = "ru-1"

# Данные для подключения к холодному хранилищу
S3_COLD_ENDPOINT = os.getenv('S3_COLD_ENDPOINT')
S3_COLD_ACCESS_KEY = os.getenv('S3_COLD_ACCESS_KEY')
S3_COLD_SECRET_KEY = os.getenv('S3_COLD_SECRET_KEY')
S3_COLD_BUCKET = os.getenv('S3_COLD_BUCKET')


def copy_all_s3_to_cold_s3():
    # Клиент для стандартного хранилища
    std_s3 = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        )
    now = get_time_msk()
    # Клиент для холодного хранилища
    cold_s3 = boto3.client(
        "s3",
        endpoint_url=S3_COLD_ENDPOINT,
        aws_access_key_id=S3_COLD_ACCESS_KEY,
        aws_secret_access_key=S3_COLD_SECRET_KEY,
        )
    
    # Получаем список объектов из стандартного хранилища
    paginator = std_s3.get_paginator("list_objects_v2")
    
    for page in paginator.paginate(Bucket=S3_BUCKET):
        if "Contents" not in page:
            continue
        
        for obj in page["Contents"]:
            key = obj["Key"]
            
            # Загружаем объект из стандартного
            response = std_s3.get_object(Bucket=S3_BUCKET, Key=key)
            data = response["Body"].read()
            
            # Кладём в холодное хранилище
            key = f'{now}/{key}'
            cold_s3.put_object(Bucket=S3_COLD_BUCKET, Key=key, Body=data)
