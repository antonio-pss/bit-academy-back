from typing import Any, BinaryIO, Dict, Optional

from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User
from core.services import MinioUploaderService


# Função para gerar tokens JWT, útil para APIs
def get_tokens_for_user(user: User) -> Dict[str, str]:
    """Gera tokens de acesso e atualização JWT para um usuário."""
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    refresh['id'] = str(user.id) # UUID precisa ser string
    refresh['email'] = user.email
    refresh['name'] = user.name
    refresh['username'] = user.username
    refresh['is_active'] = user.is_active
    refresh['date_joined'] = user.date_joined.isoformat() if user.date_joined else None
    refresh['avatar'] = user.avatar

    return {
        'access': str(access),
        'refresh': str(refresh),
    }

class AuthUser:
    def __init__(self, minio_uploader: MinioUploaderService):
        self.minio = minio_uploader

    def update_user(self, user: User, user_data: Dict[str, Any], avatar: Optional[BinaryIO] = None) -> User:
        user_data.pop('password', None)
        user_data.pop('id', None)
        user_data.pop('email', None)
        user_data.pop('username', None)

        if avatar:
            user_data['avatar'] = self.minio.handle_avatar_upload(avatar, getattr(user, 'avatar', None))

        for attr, value in user_data.items():
            if hasattr(user, attr):
                setattr(user, attr, value)

        user.save(update_fields=[*user_data.keys(), 'updated_at']) # Salva apenas os campos atualizados
        return user

    def deactivate_user(self, user: User) -> User:
        if user.is_active:
            user.is_active = False
            user.save(update_fields=['is_active', 'updated_at'])
        return user
