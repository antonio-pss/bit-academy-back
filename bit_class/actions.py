from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from guardian.shortcuts import assign_perm
from rest_framework import status, response
from bit_class.models import ClassInvitation, ClassMember, ClassRole

class PermissionUtils:
    @staticmethod
    def has_permissions(user, obj, permissions=None):
        permissions = permissions or []
        for perm in permissions:
            if not user.has_perm(perm, obj):
                raise PermissionDenied(f"Permissão '{perm}' negada para o usuário {user}.")
        return True

class ClassActions:
    @staticmethod
    @transaction.atomic
    def perform_create(serializer, request_user):
        # Valida a permissão antes de criar
        PermissionUtils.has_permissions(request_user, None, ['add_class'])
        instance = serializer.save()
        role, created = ClassRole.objects.get_or_create(role='TCHR')
        ClassMember.objects.create(
            id_class=instance,
            id_user=request_user,
            id_class_role=role
        )
        # Atribui permissões padrão
        perm_list = [
            'perform_create', 'delete_class', 'invite_user', 'accept_invitation',
            'decline_invitation', 'add_student_link', 'remove_student', 'delete_invitation_by_email'
        ]
        for perm in perm_list:
            assign_perm(perm, request_user, instance)
        return instance

    @staticmethod
    def invite_user(request, class_obj, serializer_data):
        if not request.user.has_perm('invite_user', class_obj):
            return response.Response({"error": "Você não tem permissão para convidar usuários."}, status=403)
        email = serializer_data.get('email')
        role_id = serializer_data.get('role_id')
        user = User.objects.filter(email=email).first()
        if user:
            ClassInvitation.objects.get_or_create(
                email=email,
                id_class=class_obj,
                role_id=role_id
            )
            return response.Response({"detail": "Convite enviado."})
        return response.Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def accept_invitation(request, convite_id):
        conv = ClassInvitation.objects.filter(id=convite_id, email=request.user.email).first()
        if conv and not conv.is_accepted:
            conv.is_accepted = True
            conv.save()
            ClassMember.objects.create(
                id_class=conv.id_class,
                id_user=request.user,
                id_class_role=conv.id_class_role
            )
            return response.Response({"detail": "Convite aceito."})
        return response.Response({"error": "Convite inválido ou já aceito."}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_invitation_by_email(email):
        try:
            invitation = ClassInvitation.objects.get(email=email)
            invitation.delete()
            return {"detail": f"Convite para o email {email} foi excluído com sucesso."}
        except ObjectDoesNotExist:
            return {"detail": f"Convite com email {email} não encontrado."}

    @staticmethod
    def add_student_link(request, class_obj, email):
        user = User.objects.filter(email=email).first()
        if user:
            estudante_role, _ = ClassRole.objects.get_or_create(name='Estudante')
            ClassMember.objects.create(id_class=class_obj, id_user=user, id_class_role=estudante_role)
            return response.Response({"detail": "Estudante adicionado."})
        return response.Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def remove_student(request, class_obj, user_id):
        member = ClassMember.objects.filter(
            id_class=class_obj, id_user=user_id,
            id_class_role__name='Estudante').first()
        if member:
            member.delete()
            return response.Response({"detail": "Estudante removido."})
        return response.Response({"error": "Estudante não encontrado na sala."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def decline_invitation(request, convite_id):
        conv = ClassInvitation.objects.filter(id=convite_id, email=request.user.email).first()
        if conv and not conv.is_accepted:
            conv.delete()
            return response.Response({"detail": "Convite recusado."})
        return response.Response({"error": "Convite inválido ou já aceito."}, status=status.HTTP_400_BAD_REQUEST)