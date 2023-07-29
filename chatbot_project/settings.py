"""
Django settings for chatbot_project project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from . import my_setting


# Auth account
AUTH_USER_MODEL = 'account.Account'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = my_setting.Django_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = my_setting.Django_DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "chatbot",
    "account",
]


REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASS': {
        'rest_framework.throttling.AnonRateThrottle', # 로그인 안한애
        'rest_framework.throttling.UserRateThrottle',
    },
    'DEFAULT_THROTTLE_RATES': {
        'anon':'5/hour', # sec, min, hour, day
        'user':'20/hour',
    },
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         # 'rest_framework.permissions.IsAdminUser',
#     ],
#     'DEFAULT_PAGINATION_CLASS' :'PageNumberPagination.',
#     'PAGE_SIZE': 10
# }

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
]
# CORS_ALLOWED_ORIGIN_REGEXES = [r"^https://\w+\.example\.com$",]
# CORS_ALLOW_ALL_ORIGINS = True or False
###
# CORS_ALLOW_METHODS = [  # 허용할 옵션
#     "DELETE",
#     "GET",
#     "OPTIONS",
#     "PATCH",
#     "POST",
#     "PUT",
# ]

# CORS_ALLOW_HEADERS = [ # 허용할 헤더
#     "accept",
#     "accept-encoding",
#     "authorization",
#     "content-type",
#     "dnt",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
#     # "my-header", # api요청 헤더에 추가한 것을 여기에 추가하면 읽어올 수 있습니다.
# ]
# CORS_ALLOW_CREDENTIALS = True


ROOT_URLCONF = "chatbot_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "chatbot_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# SESSION
# 세션 관련해서 어떤 세션 엔진을 사용할 것인지.
# 일반적으로 서버에서 세션을 저장할때 database에 저장합니다.
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# 세션의 유지기간
SESSION_COOKIE_AGE = 86400 # 하루 = 24h * 60m * 60s -> client(browser)

# 사용자가 브라우저 종료 시 세션을 없앨 건지. Ture면 닫을때 세션 삭제
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# server session > client session_id. 세션이 만료가 되어도 db에 저장된 세션은 사라지지않습니다. 이런 세션들이 마구 쌓이면 부하가 걸릴 것입니다. 
# 그래서 서버 쪽에서 세션을 지워줄 필요가 있습니다.
# 근데 만료된것만 지우는게 아니라 다 삭제됨
# python manage.py clearsessions -> corn (crontab) : 스케쥴 설정 가능


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
