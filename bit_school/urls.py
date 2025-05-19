from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'institutions', viewsets.InstitutionViewSet)
router.register(r'courses', viewsets.CourseViewSet)
router.register(r'modules', viewsets.ModuleViewSet)
router.register(r'disciplines', viewsets.DisciplineViewSet)
router.register(r'course-module-discipline', viewsets.CourseModuleDisciplineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]