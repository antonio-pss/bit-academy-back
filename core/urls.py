from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import viewsets

urlpatterns = [
    # Rotas de Autenticação e Usuário
    path('auth/signup/', viewsets.RegisterView.as_view(), name='auth_register'),
    path('auth/login/', viewsets.LoginView.as_view(), name='auth_login'),
    path('auth/logout/', viewsets.LogoutView.as_view(), name='auth_logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Rota padrão do simplejwt
    path('auth/user/', viewsets.UserDetailView.as_view(), name='auth_user_detail'), # Rota para detalhes/update do usuário logado
    path('accounts/', include('allauth.urls')),
]