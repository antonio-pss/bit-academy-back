from rest_framework import serializers

from bit_class.models import Class, ClassInvitation, ClassMember, ClassRole, Frequency, Status, Time, Grade, \
    TaskSubmission, Activity
from core.models import User


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'description', 'id_course_module_discipline']

    expandable_fields = {
        'id_course_module_discipline': ('CourseModuleDisciplineSerializer', {'fields': ['id', 'url', 'name']}),
    }


class ClassMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMember
        fields = ['id', 'id_class', 'id_user', 'id_class_role']

    expandable_fields = {
        'id_class': ('ClassSerializer', {'fields': ['id', 'name', 'description']}),
        'id_class_role': ('ClassRoleSerializer', {'fields': ['id', 'role']}),
        'id_user': ('core.UserSerializer', {'fields': ['id', 'email', 'username']}),  # caso queira expandir usuário
    }


class ClassInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassInvitation
        fields = ['id', 'email', 'id_class', 'id_class_role', 'is_accepted']

    expandable_fields = {
        'id_class': ('ClassSerializer', {'fields': ['id', 'name']}),
        'id_class_role': ('ClassRoleSerializer', {'fields': ['id', 'role']}),
    }


class AssignRoleSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role_id = serializers.PrimaryKeyRelatedField(queryset=ClassRole.objects.all())


class ClassRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRole
        fields = ['id', 'role', 'created', 'modified', 'is_active']


class ClassInvitationResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_accepted = serializers.BooleanField()


class ClassInvitationDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ClassInvitationAcceptSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_accepted = serializers.BooleanField(default=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=ClassRole.objects.all())
    class Meta:
        model = ClassInvitation
        fields = ['email', 'is_accepted', 'role_id']


class FrequencySerializer(serializers.ModelSerializer):
    id_class_member = ClassMemberSerializer(read_only=True)
    day = serializers.DateField()

    class Meta:
        model = Frequency
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TimeSerializer(serializers.ModelSerializer):
    id_frequency = FrequencySerializer(read_only=True)
    id_status = StatusSerializer(read_only=True)
    start_hour = serializers.DateTimeField()
    end_hour = serializers.DateTimeField()

    class Meta:
        model = Time
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class TaskSubmissionSerializer(serializers.ModelSerializer):
    id_activity = ActivitySerializer(read_only=True)
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = TaskSubmission
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    id_task_submission = TaskSubmissionSerializer(read_only=True)
    score = serializers.IntegerField()

    class Meta:
        model = Grade
        fields = '__all__'


