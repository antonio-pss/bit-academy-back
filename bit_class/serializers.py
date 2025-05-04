from rest_framework import serializers
from bit_class.models import Class, ClassMember, ClassInvitation, ClassRole


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'description', 'id_course_module_discipline']


class ClassMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMember
        fields = ['id', 'id_class', 'id_user', 'id_class_role']


class ClassInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassInvitation
        fields = ['id', 'email', 'id_class', 'role', 'is_accepted']


class AssignRoleSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role_id = serializers.PrimaryKeyRelatedField(queryset=ClassRole.objects.all())


class ClassRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRole
        fields = ['id', 'name']


class ClassInvitationResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_accepted = serializers.BooleanField()


class ClassInvitationDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField()


