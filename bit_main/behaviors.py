from typing import BinaryIO, Optional
from urllib.parse import urlparse
import uuid
from minio import Minio
from django.conf import settings


class MinioUploader:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.base_url = settings.MINIO_BASE_URL

    def upload_data_to_minio(self, file_data: BinaryIO, filename: str, bucket: str) -> Optional[str]:
        try:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)

            unique_filename = f"{uuid.uuid4()}-{filename}"

            result = self.client.put_object(
                bucket_name=bucket,
                object_name=unique_filename,
                data=file_data,
                length=file_data.size,
                content_type=file_data.content_type
            )

            return f"{self.base_url}/{bucket}/{unique_filename}"

        except Exception as e:
            print(f"Erro ao fazer upload: {str(e)}")
            return None

    def delete_data_from_minio(self, file_url: str) -> bool:
        if not file_url:
            return False

        try:
            parsed_url = urlparse(file_url)
            path_parts = parsed_url.path.strip('/').split('/')

            if len(path_parts) < 2:
                return False

            bucket = path_parts[0]
            filename = path_parts[1]

            self.client.remove_object(bucket, filename)
            return True

        except Exception as e:
            print(f"Erro ao deletar arquivo: {str(e)}")
            return False

    def handle_avatar_upload(self, avatar: BinaryIO, old_avatar: Optional[str] = None) -> Optional[str]:
        if not avatar:
            return None

        if old_avatar:
            self.delete_data_from_minio(old_avatar)

        return self.upload_data_to_minio(avatar, avatar.name, 'media')