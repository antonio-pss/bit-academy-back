from django.urls import path, include
from rest_framework import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'class', views.ClassViewSet, basename='class')

urlpatterns = [
    path('', include(router.urls)),
]