from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.conf import settings
from typing import Optional, Dict, Any, BinaryIO
import uuid
from .models import User
from .behaviors import MinioUploader


class UserService:
    def __init__(self, minio_uploader: MinioUploader):
        self.minio = minio_uploader

    def validate_user_data(self, user_data: Dict[str, Any]) -> None:
        if 'password' in user_data:
            try:
                validate_password(user_data['password'])
            except ValidationError as e:
                raise ValidationError({'password': e.messages})

        if 'email' in user_data and User.objects.filter(email=user_data['email']).exists():
            raise ValidationError({'email': ['Este email já está em uso.']})

    def create_user(self, user_data: Dict[str, Any], avatar: Optional[BinaryIO] = None) -> User:
        self.validate_user_data(user_data)
        if avatar:
            user_data['avatar'] = self.minio.handle_avatar_upload(avatar)
        user = User.objects.create(**user_data)

        # Funcionalidades futuras aqui: envio de email de boas-vindas.

        return user

    def update_user(self, user: User, user_data: Dict[str, Any], avatar: Optional[BinaryIO] = None) -> User:
        user_data.pop('password', None)

        if 'email' in user_data and user_data['email'] != user.email:
            if User.objects.filter(email=user_data['email']).exists():
                raise ValidationError({'email': ['Este email já está em uso.']})

        if avatar:
            user_data['avatar'] = self.minio.handle_avatar_upload(avatar, user.avatar)

        for attr, value in user_data.items():
            setattr(user, attr, value)

        user.save()
        return user

    def deactivate_user(self, user: User) -> User:
        user.is_active = False
        user.save()

        return user

    def change_password(self, user: User, new_password: str) -> User:
        validate_password(new_password)
        user.set_password(new_password)
        user.save()
        return user
    

class AuthUserService:
    def login_user(self, request, user: User) -> None:
        login(request, user)

    def logout_user(self, request) -> None:
        logout(request)

    def request_password_reset(self, email: str) -> Optional[str]:
        try:
            user = User.objects.get(email=email)
            token = str(uuid.uuid4())
            user.reset_password_token = token
            user.save()

            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            send_mail(
                'Reset Your Password',
                f'Click here to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return token
        except User.DoesNotExist:
            return None

    def reset_password(self, token: str, new_password: str) -> bool:
        try:
            user = User.objects.get(reset_password_token=token)
            user.set_password(new_password)
            user.reset_password_token = None
            user.save()
            return True
        except User.DoesNotExist:
            return False

