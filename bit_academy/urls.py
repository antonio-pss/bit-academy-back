from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Bit Academy API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# URLs principais do projeto
urlpatterns = [
    # Admin do Django
    path('admin/', admin.site.urls),

    # APIs
    path('api/', include([
        path('', include('bit_main.urls')),
        # path('school/', include('bit_school.urls')),
        # path('class/', include('bit_class.urls')),
        # path('notes/', include('bit_notes.urls')),
    ])),

    # Documentação da API
    path('docs/', include([
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    ])),
]

# Configurações para servir mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)