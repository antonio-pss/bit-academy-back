from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core import actions, serializers, models


class RegisterViewsets(generics.CreateAPIView):
    queryset = models.User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer

    @action(detail=False, methods=['post'])
    def create_user(validated_data):
        return Response(actions.UserActions.create_user(validated_data), status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    parser_classes = [MultiPartParser]

    @action(detail=True, methods=['POST'])
    def upload_avatar(self, request, pk=None):
        user = self.get_object()
        serializer = serializers.UserAvatarUploadSerializer(data=request.data)
        if serializer.is_valid():
            avatar_file = serializer.validated_data['avatar']
            try:
                avatar_url = actions.UserActions.handle_user_avatar_upload(user, avatar_file)
                return Response({'avatar_url': avatar_url}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewsets(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = actions.get_tokens_for_user(user)
        return Response(tokens)


class UserDetailViewsets(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False, methods=['get'])
    def get_object(self):
        return self.request.user

    @action(detail=True, methods=['PUT'], permission_classes=[permissions.IsAuthenticated])
    def update(self, request, pk=None):
        user = self.get_object()
        serializer = serializers.UpdateUserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                update = actions.SocialAccountActions.update(user, serializer.validated_data)
                return Response(serializers.UserSerializer(update).data)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        except Exception:
            return Response({"detail": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserViewsets(generics.DestroyAPIView):
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete(self, request, pk=None):
        serializer = serializers.DeleteUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = self.get_object()
            try:
                actions.SocialAccountActions.delete_user(user)
                return Response({'detail': 'Usuário excluído com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
