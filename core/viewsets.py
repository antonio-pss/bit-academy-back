from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers, actions
from .models import User
from .serializers import UserAvatarUploadSerializer


class RegisterViewsets(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer  # seu serializador de usuários
    parser_classes = [MultiPartParser]

    @action(detail=True, methods=['POST'])
    def upload_avatar(self, request, pk=None):
        user = self.get_object()
        serializer = UserAvatarUploadSerializer(data=request.data)
        if serializer.is_valid():
            avatar_file = serializer.validated_data['avatar']
            try:
                avatar_url = actions.UserActions.handle_user_avatar_upload(user, avatar_file)
                return Response({'avatar_url': avatar_url}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewsets(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = (permissions.AllowAny,)


class UserDetailViewsets(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False, methods=['get'])
    def get_object(self):
        return self.request.user

class LogoutViewsets(APIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False, methods=['post'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)


# Views para Login Social (Placeholder)
# class GoogleLoginView(APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = serializers.CustomSocialLoginSerializer # Ou talvez nenhum serializer aqui
#
#     def post(self, request, *args, **kwargs):
#         # ... lógica complexa de interação com Google e allauth ...
#         pass # Implementar

# class GithubLoginView(APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = serializers.CustomSocialLoginSerializer # Ou talvez nenhum serializer aqui
#
#     def post(self, request, *args, **kwargs):
#         # ... lógica complexa de interação com Github e allauth ...
#         pass # Implementar
