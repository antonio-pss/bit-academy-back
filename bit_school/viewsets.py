from rest_framework import viewsets
from .models import Institution, Course, Module, Discipline, CourseModuleDiscipline
from . import serializers

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = serializers.ModuleSerializer

class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = serializers.DisciplineSerializer

class CourseModuleDisciplineViewSet(viewsets.ModelViewSet):
    queryset = CourseModuleDiscipline.objects.all()
    serializer_class = serializers.CourseModuleDisciplineSerializer