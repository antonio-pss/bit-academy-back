from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from . import viewsets

urlpatterns = [
    # Rotas de Autenticação e Usuário
    path('auth/signup/', viewsets.RegisterViewsets.as_view(), name='auth_register'),
    path('auth/login/', viewsets.LoginViewsets.as_view(), name='auth_login'),
    path('auth/logout/', viewsets.LogoutViewsets.as_view(), name='auth_logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Rota padrão do simplejwt
    path('auth/user/', viewsets.UserDetailViewsets.as_view(), name='auth_user_detail'), # Rota para detalhes/update do usuário logado
    path('accounts/', include('allauth.urls')),
]
