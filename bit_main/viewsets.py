from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ValidationError
from rest_framework.throttling import AnonRateThrottle

from bit_main.models import User
from bit_main import serializers
from bit_main.behaviors import MinioUploader
from bit_main.serializers import UserSerializer
from bit_main.services import UserService, AuthUserService
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_user_service(self):
        return UserService(MinioUploader())

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_service'] = self.get_user_service()
        return context

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = serializers.ChangePasswordSerializer(
            data=request.data,
            context={'user_service': self.get_user_service()}
        )

        if serializer.is_valid():
            try:
                self.get_user_service().change_password(
                    user,
                    serializer.validated_data['new_password']
                )
                return Response({'status': 'password changed'})
            except ValidationError as e:
                return Response(
                    {'error': e.messages},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        try:
            self.get_user_service().deactivate_user(user)
            return Response({'status': 'user deactivated'})
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )


class SignupViewSet(viewsets.ViewSet):

    def get_auth_service(self):
        return UserService()

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        try:
            user = self.get_auth_service().create_user(request.data)
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginViewSet(viewsets.ViewSet):
    throttle_classes = [AnonRateThrottle]
    throttle_scope = 'login'

    def get_auth_service(self):
        return AuthUserService()

    @action(detail=False, methods=['post'])
    def login(self, request):
        try:
            credentials = {
                'email': request.data.get('email'),
                'password': request.data.get('password')
            }
            user = self.get_auth_service().login_user(credentials)
            return Response({'status': 'logged in', 'user': UserSerializer(user).data})
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def get_auth_service(self):
        return AuthUserService()
    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            self.get_auth_service().logout_user(request)
            return Response({'status': 'logged out'})
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

# class EmailVerificationViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#
#     def get_auth_service(self):
#         return AuthUserService()
#
#     @action(detail=False, methods=['post'])
#     def verify_email(self, request):
#         try:
#             self.get_auth_service().verify_email(request.data.get('token'))
#             return Response({'status': 'email verified'})
#         except ValidationError as e:
#             return Response(
#                 {'error': e.messages},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# class ForgotPasswordViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
# 
#     def get_auth_service(self):
#         return AuthUserService()
# 
#     @action(detail=False, methods=['post'])
#     def forgot_password(self, request):
#         try:
#             self.get_auth_service().forgot_password(request.data.get('email'))
#             return Response({'status': 'recovery email sent'})
#         except ValidationError as e:
#             return Response(
#                 {'error': e.messages},
#                 status=status.HTTP_400_BAD_REQUEST
#             )


# class ResetPasswordViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
# 
#     def get_auth_service(self):
#         return AuthUserService()
# 
#     @action(detail=False, methods=['post'])
#     def reset_password(self, request):
#         try:
#             self.get_auth_service().reset_password(
#                 request.data.get('token'),
#                 request.data.get('new_password')
#             )
#             return Response({'status': 'password reset successful'})
#         except ValidationError as e:
#             return Response(
#                 {'error': e.messages},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
