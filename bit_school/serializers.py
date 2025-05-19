from rest_framework import serializers

from core.models import User
from .models import InstitutionRole, Institution, UserInstitutionRole, Course, Module, Discipline, CourseModuleDiscipline

class InstitutionRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionRole
        fields = '__all__'

    expandable_fields = {
    'id_instituition_role': ('InstitutionRoleSerializer', {'fields': ['id', 'url', 'name']}),
    'id_institution': ('InstitutionSerializer', {'fields': ['id', 'url', 'name']}),
    }

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'

    expandable_fields = {
        'id_institution_role': ('InstitutionRoleSerializer', {'fields': ['id', 'url', 'name']}),
    }

class UserInstitutionRoleSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_institution = serializers.PrimaryKeyRelatedField(queryset=Institution.objects.all(), allow_null=True)
    id_institution_role = serializers.PrimaryKeyRelatedField(queryset=InstitutionRole.objects.all(), allow_null=True)

    class Meta:
        model = UserInstitutionRole
        fields = '__all__'

    expandable_fields = {
        'id_user': ('core.UserSerializer', {'fields': ['id', 'url', 'name']}),
        'id_institution': ('InstitutionSerializer', {'fields': ['id', 'url', 'name']}),
        'id_institution_role': ('InstitutionRoleSerializer', {'fields': ['id', 'url', 'name']}),
    }



class CourseSerializer(serializers.ModelSerializer):
    id_institution = serializers.PrimaryKeyRelatedField(queryset=Institution.objects.all())

    class Meta:
        model = Course
        fields = '__all__'

    expandable_fields = {
        'id_institution': ('InstitutionSerializer', {'fields': ['id', 'url', 'name']}),
    }

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

    expandable_fields = {
        'id_institution': ('InstitutionSerializer', {'fields': ['id', 'url', 'name']}),
    }


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'

    expandable_fields = {
        'id_institution': ('InstitutionSerializer', {'fields': ['id', 'url', 'name']}),
        'id_module': ('ModuleSerializer', {'fields': ['id', 'url', 'name']}),
        'id_course': ('CourseSerializer', {'fields': ['id', 'url', 'name']}),
    }


class CourseModuleDisciplineSerializer(serializers.ModelSerializer):
    id_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    id_module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())
    id_discipline = serializers.PrimaryKeyRelatedField(queryset=Discipline.objects.all())

    class Meta:
        model = CourseModuleDiscipline
        fields = '__all__'

    expandable_fields = {
        'id_course': ('CourseSerializer', {'fields': ['id', 'url', 'name']}),
        'id_module': ('ModuleSerializer', {'fields': ['id', 'url', 'name']}),
        'id_discipline': ('DisciplineSerializer', {'fields': ['id', 'url', 'name']}),
    }