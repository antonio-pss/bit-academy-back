from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import TokenError
from core import models
from core import actions

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ('email', 'name', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def create(self, validated_data):
        user = actions.UserActions.create_user(validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'name', 'username', 'xp', 'streak', 'bio', 'avatar', 'is_active', 'date_joined']
        read_only_fields = ['email', 'is_active', 'date_joined', 'id', 'xp', 'streak']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token = actions.TokenActions.add_custom_claims(token, user)
        return token


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
