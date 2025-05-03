import uuid
from typing import BinaryIO, Optional
from urllib.parse import urlparse

from django.conf import settings
from minio import Minio
from minio.error import S3Error

from core.factories import get_storage_service
from core.implementations.minio_storage import logger


class MinioUploaderService:
    def __init__(self):
        # Inicializa o cliente MinIO na instância
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.base_url = settings.MINIO_BASE_URL

    def ensure_bucket_exists(self, bucket_name: str):
        """Verifica se o bucket existe e cria se necessário."""
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
        except S3Error as e:
            # Log ou tratamento de erro
            raise

    def upload_data_to_minio(self, file_data: BinaryIO, filename: str, bucket: str) -> Optional[str]:
        try:
            # Verifica ou cria o bucket
            self.ensure_bucket_exists(bucket)

            # Gera nome de arquivo único
            unique_filename = f"{uuid.uuid4()}-{filename}"

            # Realiza o upload
            self.client.put_object(
                bucket_name=bucket,
                object_name=unique_filename,
                data=file_data,
                length=file_data.size,
                content_type=getattr(file_data, 'content_type', 'application/octet-stream')
            )

            # Retorna URL acessível
            return f"{self.base_url}/{bucket}/{unique_filename}"
        except S3Error as e:
            # Log ou tratamento de erro
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
        except S3Error as e:
            print(f"Erro ao deletar arquivo: {str(e)}")
            return False

    def handle_avatar_upload(self, avatar: BinaryIO, filename: str, old_avatar_url: Optional[str] = None) -> Optional[str]:
        # Remove avatar antigo, se existir
        if old_avatar_url:
            self.delete_data_from_minio(old_avatar_url)
        # Realiza o upload do novo avatar
        return self.upload_data_to_minio(avatar, filename, 'media')  # 'media' pode ser substituído por sua lógica

class UserService:
    def __init__(self):
        self.storage = get_storage_service()

    def update_avatar(self, user, avatar_file):
        try:
            avatar_path = self.storage.store_avatar(avatar_file, user.id)
            user.avatar = avatar_path
            user.save()
            return self.storage.get_avatar_url(avatar_path)
        except StorageError as e:
            logger.error(f"Erro ao atualizar avatar: {str(e)}")
            raise
