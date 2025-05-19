from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from . import viewsets

urlpatterns = [
    # Rotas de Autenticação e Usuário
    path('signup/', viewsets.RegisterViewsets.as_view(), name='auth_register'),
    path('login/', viewsets.LoginViewsets.as_view(), name='auth_login'),
    path('logout/', viewsets.LogoutViewsets.as_view(), name='auth_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auser/<int:pk>/', viewsets.UserDetailViewsets.as_view(), name='auth_user_detail'),
    path('accounts/', include('allauth.urls')),
]
