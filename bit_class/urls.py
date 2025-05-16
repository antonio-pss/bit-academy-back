from django.urls import include, path
from rest_framework import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'class', views.ClassViewSet, basename='class')

urlpatterns = [
    path('', include(router.urls)),
]
