import os  # Добавили этот импорт, чтобы os.path.join работал
import dj_database_url
from pathlib import Path
from datetime import timedelta

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = 'django-insecure-ha&&8q)22*^5x%xb5nq9jmx@zf!*aap5pg=gq8iz0jenld2auc'

# ВАЖНО: На Railway/Render DEBUG лучше выключать через переменные окружения
DEBUG = True 

# Добавь '*' чтобы на этапе теста не было проблем с хостами
ALLOWED_HOSTS = ['*'] 

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'products',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Разрешаем фронтенду (React) обращаться к бэкенду
CORS_ALLOW_ALL_ORIGINS = True 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', # Изменил, чтобы товары были видны без логина
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'LOGIN_FIELD': 'username',
}

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# Эта настройка заставит Django использовать SQLite дома и Postgres на Railway
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Настройка для картинок (Media)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'raceawm@gmail.com'
EMAIL_HOST_PASSWORD = 'klur ilel kcla vlwo'
# 1. Список доверенных источников для CSRF (ОБЯЗАТЕЛЬНО для работы POST/заказов)
# Сюда нужно вставить URL вашего фронтенда на Vercel
CSRF_TRUSTED_ORIGINS = [
    "https://sezim-frontend.vercel.app",
    "https://sezim-frontend-k3wn5xaid-samgar-24s-projects.vercel.app",
    "https://sezim-frontend-5kkosunkm-samgar-24s-projects.vercel.app", # Добавьте основной домен, если он есть
]

# 2. Настройка CORS (уточнение)
# Хотя ALLOW_ALL_ORIGINS работает, для безопасности в продакшене лучше использовать:
CORS_ALLOWED_ORIGINS = [
    "https://sezim-frontend-k3wn5xaid-samgar-24s-projects.vercel.app",
    "https://sezim-frontend.vercel.app",
    "https://sezim-frontend-k3wn5xaid-samgar-24s-projects.vercel.app",
    "https://sezim-frontend-5kkosunkm-samgar-24s-projects.vercel.app",
    
]

# 3. Разрешить передачу учетных данных (куки, заголовки авторизации)
CORS_ALLOW_CREDENTIALS = True

# 4. Безопасность (рекомендуется для Railway)
# Если ваш бэкенд работает через HTTPS (у Railway это так)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True