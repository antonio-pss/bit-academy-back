from django.urls import path
from bit_class import viewsets

urlpatterns = [
    # Rotas de CRUD para as classes
    path('new/', viewsets.ClassViewSet.as_view({'get': 'list', 'post': 'create'}), name='class'),
    path('<int:pk>/', viewsets.ClassViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='class-detail'),
]
