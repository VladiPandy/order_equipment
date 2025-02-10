
from pathlib import Path
import os

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

include(
    'components/database.py',
)

SECRET_KEY = ''

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:8081',]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'control_enter.apps.ControlEnterConfig',
    'basic_elements.apps.BasicElementsConfig',
    'dependings.apps.DependingsConfig',
    'admin_reorder',
    'user_auth',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',


    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'user_auth.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

LOCALE_PATHS = ['config/locale']

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Например, если у вас есть папка static в корне проекта
]

STATIC_URL = '/static/'

ADMIN_REORDER = (
    { 'app': 'auth' },
    {
        'app': 'basic_elements',
        'label': 'Базовые настройки'
    },
    {
        'app': 'control_enter',
        'label': 'Настройки доступа системы'
    },
    {
        'app': 'dependings',
        'label': 'Настройка взаимосвязей'
    }
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'        # после успешного входа перенаправляем на главную страницу
LOGOUT_REDIRECT_URL = '/logout/'  #

# Дополнительные URL, для которых не требуется авторизация
LOGIN_EXEMPT_URLS = [
    '/login/',
    '/register/',
    '/logout/',
    '/static/',  # если статика не обслуживается веб-сервером напрямую
]