from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from guardian.shortcuts import assign_perm
from rest_framework import status, response


from bit_class.models import ClassInvitation, ClassMember, ClassRole


class ClassActions:

    @staticmethod
    @transaction.atomic
    def perform_create(serializer, request_user):
        instance = serializer.save()
        role, created = ClassRole.objects.get_or_create(role='TCHR')
        ClassMember.objects.create(
            id_class=instance,
            id_user=request_user,
            id_class_role=role
        )
        # Permissions
        # implementar regra para caso de: se o usuário que possua o atributo 'role' da sala de aula como 'TCHR' ou PRIN, queira sair da sala, obrigatoriamente selecionar outro usuário para ser professor se não houver nenhum outro usuário 'TCHR' ou 'PRIN'.
        assign_perm('delete_class', request_user, instance)
        assign_perm('invite_user', request_user, instance)
        assign_perm('accept_invitation', request_user, instance)
        assign_perm('decline_invitation', request_user, instance)
        assign_perm('add_student_link', request_user, instance)
        assign_perm('remove_student', request_user, instance)
        assign_perm('delete_invitation_by_email', request_user, instance)

        return instance

    @staticmethod
    def invite_user(request, class_obj, serializer_data):
        if not request.user.has_perm('invite_user', class_obj):
            return response.Response({"error": "Você não tem permissão para convidar usuários."}, status=403)
        else:
            email = serializer_data.get('email')
            role_id = serializer_data.get('role_id')
            user = User.objects.filter(email=email).first()

        if user:
            invite, created = ClassInvitation.objects.get_or_create(
                email=email,
                id_class=class_obj,
                role_id=role_id
            )
            # Aqui pode-se colocar lógica de notificação, se necessário
            return response.Response({"detail": "Convite enviado."})
        else:
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
                id_class_role=conv.role
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
        from rest_framework import status
        from rest_framework.response import Response
        user = User.objects.filter(email=email).first()
        if user:
            from bit_class.models import ClassRole
            estudante_role, _ = ClassRole.objects.get_or_create(name='Estudante')
            ClassMember.objects.create(id_class=class_obj, id_user=user, id_class_role=estudante_role)
            return Response({"detail": "Estudante adicionado."})
        else:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def remove_student(request, class_obj, user_id):
        from rest_framework import status
        from rest_framework.response import Response
        member = ClassMember.objects.filter(
            id_class=class_obj, id_user=user_id,
            id_class_role__name='Estudante').first()
        if member:
            member.delete()
            return Response({"detail": "Estudante removido."})
        return Response({"error": "Estudante não encontrado na sala."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def decline_invitation(request, convite_id):
        conv = ClassInvitation.objects.filter(id=id, email=request.user.email).first()
        if conv and not conv.is_accepted:
            conv.delete()
            return response.Response({"detail": "Convite recusado."})
        return response.Response({"error": "Convite inválido ou já aceito."}, status=status.HTTP_400_BAD_REQUEST)
