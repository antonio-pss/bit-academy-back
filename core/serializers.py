from rest_framework import serializers, generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import TokenError

from core import actions, models
from core.models import User


class RegisterViewsets(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Cria o usuário
        user_serializer = serializers.UserSerializer(user)  # Serializa o usuário criado
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


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


