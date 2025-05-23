from rest_framework import viewsets
from rest_framework.decorators import action

from bit_class.models import Class

from . import actions
from .serializers import ClassSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def perform_create(self, serializer):
        actions.ClassActions.perform_create(serializer, self.request.user)

    @action(detail=True, methods=['post'])
    def invite_user(self, request, pk=None):
        class_obj = self.get_object()
        return actions.ClassActions.invite_user(request, class_obj, request.data)

    @action(detail=True, methods=['post'])
    def accept_invite(self, request, pk=None):
        invite_id = request.data.get('invite_id')
        return actions.ClassActions.accept_invite(request, invite_id)

    @action(detail=True, methods=['post'])
    def add_student_via_link(self, request, pk=None):
        class_obj = self.get_object()
        email = request.data.get('email')
        return actions.ClassActions.add_student_via_link(request, class_obj, email)

    @action(detail=True, methods=['delete'])
    def remove_student(self, request, pk=None):
        class_obj = self.get_object()
        user_id = request.data.get('user_id')
        return actions.ClassActions.remove_student(request, class_obj, user_id)
