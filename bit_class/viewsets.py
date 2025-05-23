from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from bit_class import models
from bit_class import serializers
from . import actions

class ClassViewSet(viewsets.ModelViewSet):
    queryset = models.Class.objects.all()
    serializer_class = serializers.ClassSerializer

    @action(detail=False, methods=['post'])
    def perform_create(self, serializer):
        actions.ClassActions.perform_create(serializer, self.request.user)

    @action(detail=True, methods=['post'])
    def invite_user(self, request, pk=None):
        class_obj = self.get_object()
        return actions.ClassActions.invite_user(request, class_obj, request.data)

    @action(detail=True, methods=['post'])
    def accept_invite(self, request, pk=None):
        invite_id = request.data.get('invite_id')
        return actions.ClassActions.accept_invitation(request, invite_id)

    @action(detail=True, methods=['post'])
    def add_student_via_link(self, request, pk=None):
        class_obj = self.get_object()
        email = request.data.get('email')
        return actions.ClassActions.add_student_link(request, class_obj, email)

    @action(detail=True, methods=['delete'])
    def remove_student(self, request, pk=None):
        class_obj = self.get_object()
        user_id = request.data.get('user_id')
        return actions.ClassActions.remove_student(request, class_obj, user_id)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        role = self.get_object()
        role.is_active = not role.is_active
        role.save()
        return Response({'status': 'toggled', 'is_active': role.is_active})


class ClassMemberViewSet(viewsets.ModelViewSet):
    queryset = models.ClassMember.objects.all()
    serializer_class = serializers.ClassMemberSerializer

    def get_queryset(self):
        # Opcional: filtra os membros por classe ou usuário, se necessário
        queryset = super().get_queryset()
        class_id = self.request.query_params.get('class_id')
        if class_id:
            queryset = queryset.filter(id_class=class_id)
        return queryset


class ClassInvitationViewSet(viewsets.ModelViewSet):
    queryset = models.ClassInvitation.objects.all()
    serializer_class = serializers.ClassInvitationSerializer

    @action(detail=False, methods=['post'])
    def respond(self, request):
        serializer = serializers.ClassInvitationResponseSerializer(data=request.data)
        if serializer.is_valid():
            # Lógica para aceitar ou rejeitar convite
            return actions.ClassActions.respond_to_invitation(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete_by_email(self, request):
        serializer = serializers.ClassInvitationDeleteSerializer(data=request.data)
        if serializer.is_valid():
            return actions.ClassActions.delete_invitation_by_email(serializer.validated_data['email'])
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def accept_invitation(self, request):
        serializer = serializers.ClassInvitationAcceptSerializer(data=request.data)
        if serializer.is_valid():
            return actions.ClassActions.accept_invitation(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def decline_invitation(self, request):
        serializer = serializers.ClassInvitationResponseSerializer(data=request.data)
        if serializer.is_valid():
            return actions.ClassActions.decline_invitation(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)