import boto3 #pip install boto3
from config import get_bucket_name_toBucketYAcloud, get_aws_access_key_id, get_aws_secret_access_key

#2заливаем в хранилище яндекс

def toBucket(object_key):
    #object_key = '1234.ogg'
    bucket_name = get_bucket_name_toBucketYAcloud()
    os = boto3.client(
        's3',
        aws_access_key_id = get_aws_access_key_id(),
        aws_secret_access_key = get_aws_secret_access_key(),
        region_name = 'ru-central1',
        endpoint_url = 'https://storage.yandexcloud.net'
    )

    #1 аргумент путь до файла, 3 аргумент позволяет скачать как есть вместе с папкой
    url_to_download = os.upload_file('audio/' + object_key,bucket_name,object_key)

    response = os.head_object(Bucket=bucket_name, Key=object_key)
    print(response)

    object_url = f"https://{bucket_name}.storage.yandexcloud.net/{object_key}"
    print("URL загруженного объекта:", object_url)
    return object_url