import datetime
import os
from typing import Optional

import boto3
from botocore.exceptions import NoCredentialsError

# 配置MinIO连接参数,这里API的默认端口与web管理界面的端口不一致
MINIO_ENDPOINT = 'http://localhost'  # MinIO服务器地址
MINIO_PORT = 9000  # MinIO服务端口
ACCESS_KEY = ''  # MinIO的访问密钥
SECRET_KEY = ''  # MinIO的秘密密钥
BUCKET_NAME = 'uav-mapping'  # 目标桶的名称

# 配置boto3客户端
s3_client = boto3.client(
    's3',
    endpoint_url=f'{MINIO_ENDPOINT}:{MINIO_PORT}',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=boto3.session.Config(signature_version='s3v4')
)


def create_directory(bucket_name: str) -> str:
    """
    创建或获取当前日期的目录，如果不存在则创建。
    :param bucket_name: MinIO桶的名称
    :return: 当前日期的目录名称
    """
    now = datetime.datetime.now()
    current_directory_name = now.strftime("%Y%m")  # 格式化当前日期

    try:
        # 检查目录是否存在，不存在则进行创建
        objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=current_directory_name + '/')

        if 'Contents' in objects:
            for obj in objects['Contents']:
                if obj['Key'] == current_directory_name + '/':
                    print(f"目录 '{current_directory_name}' 已存在。")
                    return current_directory_name

        # 目录不存在，创建目录
        s3_client.put_object(Bucket=bucket_name, Key=current_directory_name + '/')
        print(f"目录 '{current_directory_name}' 已成功创建在桶 '{bucket_name}' 中。")
        return current_directory_name
    except NoCredentialsError:
        print("凭证错误")
    except Exception as e:
        print(f"目录检查或创建失败: {e}")


def upload_file(file_path: str, bucket_name: str) -> Optional[str]:
    """
    上传文件到MinIO服务器，使用特定的命名格式，并将文件放置在对应的日期目录中。
    :param file_path: 本地文件路径
    :param bucket_name: MinIO桶的名称
    :return: 文件的URL，如果上传失败则返回 None
    """
    directory_name = create_directory(bucket_name)
    if not directory_name:
        print("无法获取目录名称，上传文件失败。")
        return None

    now = datetime.datetime.now()
    custom_file_name = now.strftime("%Y%m%d%H%M")  # 根据当前时间生成自定义的文件名格式

    file_name, file_extension = os.path.splitext(file_path)
    custom_file_path = f"{custom_file_name}{file_extension}"  # 构建包含时间格式的新文件名

    try:
        object_name = f'{directory_name}/{os.path.basename(custom_file_path)}'  # 使用目录名称和自定义文件名
        s3_client.upload_file(file_path, bucket_name, object_name)  # 使用原始文件路径进行上传

        # 获取文件URL
        file_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=3600  # 生成的URL有效期（秒）
        )
        return file_url
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except NoCredentialsError:
        print("凭证错误")
    except Exception as e:
        print(f"上传失败: {e}")

    return None


# 使用示例
if __name__ == "__main__":

    local_file_path = r'D:\GeoServer\data_dir\shanghai\shanghai.tif'  # 本地文件路径
    file_url = upload_file(local_file_path, BUCKET_NAME)

    if file_url:
        print(f"文件已上传到: {file_url}")
