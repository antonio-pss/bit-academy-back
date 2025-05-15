import os
from datetime import timedelta
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = ".env.development"
env_path = BASE_DIR / ENV_FILE
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print(f"Warning: Environment file '{env_path}' não encontrado.")

ENVIRONMENT = os.getenv("DJANGO_ENV", "development")
DEBUG = os.getenv("DEBUG", "True") == "True"

def validar_env_var(var, default=None, obrigatorio=True):
    valor = os.getenv(var, default)
    if obrigatorio and valor is None:
        print(f"Warning: Variável de ambiente '{var}' não está definida.")
        if not DEBUG:
            raise RuntimeError(f"Variável obrigatória '{var}' não definida em produção.")
    return valor

SECRET_KEY = validar_env_var('SECRET_KEY', 'django-insecure-fallback-key-for-dev-only')
if SECRET_KEY == 'django-insecure-fallback-key-for-dev-only' and not DEBUG:
    raise ValueError("SECRET_KEY deve ser definido em variáveis de ambiente em produção!")

ALLOWED_HOSTS = validar_env_var("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# --- Aplicações Instaladas ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    "drf_yasg",
    'corsheaders',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    "core",
    "bit_class",
    "bit_notes",
    "bit_school",
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = "bit_academy.urls"

# --- Autenticação ---
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
AUTH_USER_MODEL = 'core.User'

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bit_academy.wsgi.application"

# --- Validadores de Senha ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# --- Banco de Dados ---
if ENVIRONMENT == "production":
    DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"), conn_max_age=600)}
else:
    # Variáveis de ambiente para o banco de desenvolvimento
    db_engine = os.getenv('ENGINE_DB', 'django.db.backends.postgresql')
    DATABASES = {
        'default': {
            'ENGINE': db_engine,
            'NAME': validar_env_var('POSTGRES_DB', 'local_db'),
            'USER': validar_env_var('POSTGRES_USER', 'local_user'),
            'PASSWORD': validar_env_var('POSTGRES_PASSWORD', 'local_password'),
            'HOST': validar_env_var('POSTGRES_HOST', 'localhost'),
            'PORT': validar_env_var('POSTGRES_PORT', '5433'),
        }
    }

# --- REST Framework ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

# --- Simple JWT ---
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_LIFETIME_MINUTES', '60'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_REFRESH_LIFETIME_DAYS', '7'))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# --- Internacionalização ---
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --- Static files (WhiteNoise) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
CORS_ALLOW_CREDENTIALS = True

# --- Minio ---
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "media")
MINIO_SECURE = os.getenv("MINIO_SECURE", "False") == "True"
MINIO_BASE_URL = os.getenv('MINIO_BASE_URL', f"{'https://' if MINIO_SECURE else 'http://'}{MINIO_ENDPOINT}")

# --- django-allauth ---
SITE_ID = 1
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'confirm_password*']
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'secret': os.getenv('GOOGLE_SECRET_KEY', ''),
            'key': '',
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
    'github': {
        'APP': {
            'client_id': os.getenv('GITHUB_CLIENT_ID', ''),
            'secret': os.getenv('GITHUB_SECRET_KEY', ''),
        },
        'SCOPE': [
            'user:email',
        ],
    }
}