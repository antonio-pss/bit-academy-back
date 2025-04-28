from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from bit_main import viewsets

# Criar routers separados por funcionalidade 
router = DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'signup', viewsets.SignupViewSet, basename='signup')
router.register(r'login', viewsets.LoginViewSet, basename='login')
router.register(r'logout', viewsets.LogoutViewSet, basename='logout')

urlpatterns = [
    # API Version 1
    path('', include([
        # Autenticação
        path('token/', viewsets.CustomTokenObtainPairView.as_view(), name='token_obtain'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('login/', viewsets.LoginViewSet.as_view({'post': 'login'}), name='login'),
        path('signup/', viewsets.SignupViewSet.as_view({'post': 'register'}), name='signup'),
        path('logout/', viewsets.LogoutViewSet.as_view({'post': 'logout'}), name='logout'),
        # Verificação de Email (a ser implementado)
        # path('email/verify/', viewsets.EmailVerificationViewSet.as_view({'post': 'verify_email'}), name='verify_email'),
        #
        # # Gerenciamento de Senha (a ser implementado)
        # path('password/forgot/', viewsets.ForgotPasswordViewSet.as_view({'post': 'forgot_password'}),
        #      name='forgot_password'),
        # path('password/reset/', viewsets.ResetPasswordViewSet.as_view({'post': 'reset_password'}),
        #      name='reset_password'),
    ])),
]
