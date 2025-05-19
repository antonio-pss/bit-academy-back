from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import TokenError

from core import actions, models


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['email', 'name', 'username', 'password']
        read_only_fields = ['id', 'created', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return actions.UserActions.create_user(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'name', 'username', 'password', 'avatar', 'is_active', 'created', 'xp', 'streak']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token = actions.TokenActions.add_custom_claims(token, user)
        return token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Credenciais inválidas.')

        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
    default_error_messages = {
        'bad_token': ('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            actions.TokenActions.blacklist_token(self.token)
        except TokenError:
            self.fail('bad_token')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'name', 'username', 'password', 'avatar']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'username': {'required': True},
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        validated_data.pop('id', None)
        validated_data.pop('is_active', None)
        validated_data.pop('created', None)
        validated_data.pop('xp', None)
        validated_data.pop('streak', None)
        return actions.UserActions.update(instance, validated_data)


class DeleteUserSerializer(serializers.Serializer):

    def validate(self, data):
        request = self.context.get('request')
        user_id = self.context['view'].kwargs.get('pk')
        if request.user.id != int(user_id):
            raise serializers.ValidationError('Permissão negada.')
        return data


class CustomSocialLoginSerializer(serializers.Serializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            actions.SocialAccountActions.handle_social_login(validated_data)
        except serializers.ValidationError:
            raise
        except Exception as e:
            raise serializers.ValidationError(f"Social login processing failed: {e}")

        return validated_data


class UserAvatarUploadSerializer(serializers.Serializer):
    avatar = serializers.ImageField()


class ClassFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    filename = serializers.CharField()


