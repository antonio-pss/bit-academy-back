from django.conf import settings
from minio import Minio

from .implementations.minio_storage import MinioStorage


def get_storage_service():
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

    return MinioStorage(minio_client)
