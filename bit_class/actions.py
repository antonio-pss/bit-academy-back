# actions.py
from django.db import transaction

from bit_class.models import Class, ClassMember, ClassInvitation, ClassRole
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import User


class ClassActions:

    @staticmethod
    @transaction.atomic
    def perform_create(serializer, request_user):
        instance = serializer.save()
        role, _ = ClassRole.objects.get_or_create(defaults={'role': 'TCHR'})[0]
        ClassMember.objects.create(
            id_class=instance,
            id_user=request_user,
            id_class_role=role
        )

        # Permissions
        assign_perm('add_class', request_user, instance)
        assign_perm('change_class', request_user, instance)
        assign_perm('delete_class', request_user, instance)
        assign_perm('view_class', request_user, instance)
        assign_perm('invite_user', request_user, instance)
        assign_perm('accept_invite', request_user, instance)
        assign_perm('add_student_via_link', request_user, instance)
        assign_perm('remove_student', request_user, instance)

        return instance

    @staticmethod
    def invite_user(request, class_obj, serializer_data):
        from rest_framework.response import Response
        from rest_framework import status
        email = serializer_data.get('email')
        role_id = serializer_data.get('role_id')
        user = User.objects.filter(email=email).first()

        if user:
            from bit_class.models import ClassInvitation
            invite, created = ClassInvitation.objects.get_or_create(
                email=email,
                id_class=class_obj,
                role_id=role_id
            )
            # Aqui pode-se colocar lógica de notificação, se necessário
            return Response({"detail": "Convite enviado."})
        else:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def aceitar_convite(request, convite_id):
        from rest_framework.response import Response
        from rest_framework import status
        conv = ClassInvitation.objects.filter(id=convite_id, email=request.user.email).first()
        if conv and not conv.is_accepted:
            conv.is_accepted = True
            conv.save()
            ClassMember.objects.create(
                id_class=conv.id_class,
                id_user=request.user,
                id_class_role=conv.role
            )
            return Response({"detail": "Convite aceito."})
        return Response({"error": "Convite inválido ou já aceito."}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def adicionar_estudante_link(request, class_obj, email):
        from rest_framework.response import Response
        from rest_framework import status
        user = User.objects.filter(email=email).first()
        if user:
            from bit_class.models import ClassRole
            estudante_role, _ = ClassRole.objects.get_or_create(name='Estudante')
            ClassMember.objects.create(id_class=class_obj, id_user=user, id_class_role=estudante_role)
            return Response({"detail": "Estudante adicionado."})
        else:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def remover_estudante(request, class_obj, user_id):
        from rest_framework.response import Response
        from rest_framework import status
        membro = ClassMember.objects.filter(id_class=class_obj, id_user=user_id,
                                            id_class_role__name='Estudante').first()
        if membro:
            membro.delete()
            return Response({"detail": "Estudante removido."})
        return Response({"error": "Estudante não encontrado na sala."}, status=status.HTTP_404_NOT_FOUND)