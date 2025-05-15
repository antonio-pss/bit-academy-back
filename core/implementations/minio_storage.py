import logging
from typing import BinaryIO
from django.conf import settings
from minio import Minio

logger = logging.getLogger(__name__)

class MinioStorage:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL
        )
        self.bucket = settings.MINIO_BUCKET
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def store_file(self, file: BinaryIO, path: str) -> str:
        try:
            file.seek(0, 2)  # Vai para o final do arquivo
            size = file.tell()
            file.seek(0)     # Volta ao início
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=path,
                data=file,
                length=size
            )
            return path
        except Exception as e:
            logger.error(f"Erro ao armazenar arquivo no MinIO: {str(e)}")
            raise e

    def delete_file(self, path: str) -> bool:
        try:
            self.client.remove_object(self.bucket, path)
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar arquivo do MinIO: {str(e)}")
            return False

    def store_avatar(self, avatar: BinaryIO, user_id: int) -> str:
        path = f"avatars/user_{user_id}/{avatar.name}"
        return self.store_file(avatar, path)

    def get_avatar_url(self, avatar_path: str) -> str:
        try:
            return f"{settings.MINIO_BASE_URL}/{self.bucket}/{avatar_path}"
        except Exception as e:
            logger.error(f"Erro ao gerar URL do avatar: {str(e)}")
            return ""

    def store_class_file(self, file: BinaryIO, filename: str, class_id: int) -> str:
        path = f"classes/class_{class_id}/{filename}"
        return self.store_file(file, path)

    def get_file_url(self, file_path: str) -> str:
        try:
            return f"{settings.MINIO_BASE_URL}/{self.bucket}/{file_path}"
        except Exception as e:
            logger.error(f"Erro ao gerar URL do arquivo: {str(e)}")
            return ""