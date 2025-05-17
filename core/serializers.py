from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import TokenError

from core import actions, models
from core.models import User


class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True, max_length=30)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = actions.UserActions.create_user(validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        read_only_fields = ['email', 'is_active', 'date_joined', 'id', 'xp', 'streak']
        write_only_fields = ['password']


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
        model = User
        fields = ['id', 'email', 'name', 'username', 'password', 'avatar']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'username': {'required': True},
            'password': {'write_only': True},
        }


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


