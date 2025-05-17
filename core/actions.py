from typing import Dict

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .services import MinioUploaderService
from .utils import process_social_account_picture


class UserActions:
    """Ações relacionadas a usuários."""

    @staticmethod
    def validate_password_match(password, confirm_password):
        """Verifica se as duas senhas fornecidas são iguais."""
        if password != confirm_password:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

    @staticmethod
    def validate_password_strength(password):
        """Valida a força da senha usando validadores do Django."""
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

    @staticmethod
    def create_user(validated_data):
        email = validated_data['email']
        name = validated_data['name']
        username = validated_data['username']
        password = validated_data['password']
        user = User.objects.create_user(
            id=validated_data.get('id'),
            email=email,
            username=username,
            name=name,
            password=password
        )
        return user

    def get_tokens_for_user(user: User) -> Dict[str, str]:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        refresh['id'] = str(user.id)  # UUID precisa ser string
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

    @staticmethod
    def handle_user_avatar_upload(user, avatar_file):
        minio_service = MinioUploaderService()
        avatar_url = minio_service.handle_avatar_upload(avatar_file, avatar_file.name, getattr(user, 'avatar', None))
        user.avatar = avatar_url
        user.save(update_fields=['avatar'])
        return avatar_url


class TokenActions:
    """Ações relacionadas a tokens JWT."""

    @staticmethod
    def add_custom_claims(token, user):
        """Adiciona claims customizadas ao payload do token JWT."""
        token['name'] = user.name
        return token

    @staticmethod
    def blacklist_token(refresh_token_value):
        """Adiciona um refresh token à blacklist."""
        try:
            RefreshToken(refresh_token_value).blacklist()
        except TokenError:
            raise TokenError('Token is invalid or expired')


class SocialAccountActions:
    """Ações relacionadas a contas sociais (ex: Google, Github)."""

    @staticmethod
    def process_social_picture(user, extra_data):
        """Processa e salva a imagem de perfil vinda de um provedor social."""
        process_social_account_picture(user, extra_data)

    @staticmethod
    def handle_social_login(validated_data):
        """
        Processa os dados validados do serializer de login social.
        (Esta é uma função placeholder, a lógica real depende do fluxo OAuth)
        """
        login = validated_data.get('login')
        if login:
            extra_data = login.account.extra_data
            SocialAccountActions.process_social_picture(login.user, extra_data)
            return login.user
        else:
            raise serializers.ValidationError("Social login data is missing.")

    @staticmethod
    def update(user, validated_data):
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.save()
        return user

    @staticmethod
    def delete_user(user):
        user.delete()
