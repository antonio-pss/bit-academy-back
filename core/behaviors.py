import logging
import uuid
from typing import Optional, BinaryIO

from minio import Minio, S3Error
from psycopg2 import DatabaseError

from bit_academy import settings

logger = logging.getLogger(__name__)

class MinioStorageBehavior:
    def __init__(self):
        self.client = self.get_storage_service()
        self.bucket = settings.MINIO_BUCKET
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def get_storage_service(self):
        """
        Returns:
            AvatarStorageInterface: Instância do serviço de armazenamento
        """
        minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )

        return MinioStorageBehavior(minio_client)

    def storage_file(self, file_data: BinaryIO, filename: str, bucket: str) -> Optional[str]:
        try:
            # Verifica ou cria o bucket
            self.ensure_bucket_exists(bucket)

            # Gera nome de arquivo único
            unique_filename = f"{uuid.uuid4()}-{filename}"

            def handle_avatar_upload(self, avatar: BinaryIO, filename: str, old_avatar_url: Optional[str] = None) -> \
                    Optional[str]:
                # Remove avatar antigo, se existir
                if old_avatar_url:
                    self.delete_data_from_minio(old_avatar_url)
                # Realiza o upload do novo avatar
                return self.upload_data_to_minio(avatar, filename,
                                                 'media')  # 'media' pode ser substituído por sua lógica

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

    def ensure_bucket_exists(self, bucket_name: str):
        """Verifica se o bucket existe e cria se necessário."""
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
        except S3Error:
            # Log ou tratamento de erro
            raise

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

    def update_avatar(self, user, avatar_file):
        try:
            avatar_path = self.storage.store_avatar(avatar_file, user.id)
            user.avatar = avatar_path
            user.save()
            return self.storage.get_avatar_url(avatar_path)
        except DatabaseError as e:
            logger.error(f"Erro ao atualizar avatar: {str(e)}")
            raise

    def run(self, file_data, filename, bucket):
        """
        Executa toda a cadeia de operações: garante o bucket, faz o upload,
        e retorna a URL do arquivo.
        """
        # Passa o bucket
        self.ensure_bucket_exists(bucket)
        # Faz o upload
        file_path = self.storage_file(file_data, filename, bucket)
        # Gera e retorna a URL
        return self.get_file_url(file_path)