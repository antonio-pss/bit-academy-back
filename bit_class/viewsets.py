from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from guardian.shortcuts import assign_perm, get_perms_for_model, get_objects_for_user
from bit_class.models import Class, ClassMember, ClassInvitation, ClassRole
from bit_class.serializers import ClassSerializer, ClassMemberSerializer, ClassInvitationSerializer, AssignRoleSerializer
from django.contrib.auth.models import Group

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def perform_create(self, serializer):
        # Cria a sala e adiciona o criador como membro com papel de professor/administrador
        instance = serializer.save()
        user = self.request.user
        role = ClassRole.objects.get_or_create(name='Professor')[0]  # ou outro papel padrão
        ClassMember.objects.create(id_class=instance, id_user=user, id_class_role=role)
        assign_perm('change_class', user, instance)
        assign_perm('delete_class', user, instance)
        assign_perm('view_class', user, instance)

    @action(detail=True, methods=['post'])
    def convidar_usuario(self, request, pk=None):
        # Envia convite para usuário por email
        class_obj = self.get_object()
        serializer = AssignRoleSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            role_id = serializer.validated_data['role_id']
            user = User.objects.filter(email=email).first()
            if user:
                # Cria o convite
                convite, criado = ClassInvitation.objects.get_or_create(
                    email=email,
                    id_class=class_obj,
                    role=role_id
                )
                # Notifica o usuário via email ou sistema interno
                return Response({"detail": "Convite enviado."})
            else:
                return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def aceitar_convite(self, request, pk=None):
        # Usuário aceita convite
        convite_id = request.data.get('convite_id')
        conv = ClassInvitation.objects.filter(id=convite_id, email=request.user.email).first()
        if conv and not conv.is_accepted:
            conv.is_accepted = True
            conv.save()
            # Cria a associação na sala
            ClassMember.objects.create(
                id_class=conv.id_class,
                id_user=request.user,
                id_class_role=conv.role
            )
            return Response({"detail": "Convite aceito."})
        return Response({"error": "Convite inválido ou já aceito."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def adicionar_estudante_link(self, request, pk=None):
        # Adiciona estudante via link único
        class_obj = self.get_object()
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            estudante_role = ClassRole.objects.get_or_create(name='Estudante')[0]
            ClassMember.objects.create(id_class=class_obj, id_user=user, id_class_role=estudante_role)
            return Response({"detail": "Estudante adicionado."})
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remover_estudante(self, request, pk=None):
        class_obj = self.get_object()
        user_id = request.data.get('user_id')
        membro = ClassMember.objects.filter(id_class=class_obj, id_user=user_id, id_class_role__name='Estudante').first()
        if membro:
            membro.delete()
            return Response({"detail": "Estudante removido."})
        return Response({"error": "Estudante não encontrado na sala."}, status=status.HTTP_404_NOT_FOUND)
