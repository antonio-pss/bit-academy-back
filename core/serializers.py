from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import TokenError
from core import models
from core import actions

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, max_length=30)
    username = serializers.CharField(required=True, max_length=20)

    class Meta:
        model = models.User
        fields = ('email', 'name', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        actions.UserActions.validate_password_strength(attrs['password'])
        return attrs

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


class MinionStorageSerializer(serializers.Serializer):
    file = serializers.FileField()
    filename = serializers.CharField()
    class_id = serializers.IntegerField()

    def validate(self, attrs):
        if not attrs.get('file'):
            raise serializers.ValidationError("File is required.")
        if not attrs.get('filename'):
            raise serializers.ValidationError("Filename is required.")
        if not attrs.get('class_id'):
            raise serializers.ValidationError("Class ID is required.")
        return attrs


class ClassFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    filename = serializers.CharField()
