import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
INTERNAL_IPS = config('INTERNAL_IPS', default='127.0.0.1', cast=Csv())

REMINDER_TASK_TOKEN = config('REMINDER_TASK_TOKEN')
REMINDER_EMAIL_TO = config("REMINDER_EMAIL_TO", cast=Csv())
WORD_MEANING_EMAIL_TO = config("WORD_MEANING_EMAIL_TO", cast=Csv())

# mail
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ckeditor_5',
    'mamood_django_admin_log_viewer',
    'import_export',

    # apps
    'general',
    'book_reading',
    'writing_plan',
    'exam_management',
    'literature',
    'document',
    'guide',
    'BookCollection',
]

SITE_TITLE_TEXT = f"{config('SITE_OWNER')}'s Study Tracker"

JAZZMIN_SETTINGS = {
    "site_title": SITE_TITLE_TEXT,
    "site_header": SITE_TITLE_TEXT,
    "site_brand": SITE_TITLE_TEXT,
    "welcome_sign": "Welcome to the Dashboard",
    "site_icon": "images/fav.png",
    "site_logo": "images/logo.png",
    "login_logo": "images/login_logo.png",
    "show_theme_chooser": True,
    "welcome_sign": "Welcome to Study Management Dashboard",
    "language_chooser": True,
    "icons": {
        "auth.user": "fas fa-user",
        "book_reading.book": "fas fa-book-open",
        "book_reading.course": "fa-solid fa-school",
        "book_reading.readingProgress": "fa fa-sliders",
        "book_reading.otherStudyProgress": "fa fa-sliders",
        "book_reading.readingPlan": "fa fa-fire",
        "book_reading.revise": "fa fa-exchange",
        "document.document": "fa fa-clone",
        "document.genre": "fa fa-navicon",
        "document.link": "fa fa-external-link-square",
        "exam_management.exam": "fa fa-puzzle-piece",
        "exam_management.improve": "fa-solid fa-arrow-up-right-dots",
        "general.notes": "fa fa-sticky-note",
        "general.studyNote": "fa fa-sticky-note",
        "writing_plan.writingPlan": "fa fa-edit",
        "literature.author": "fa fa-address-book",
        "literature.genre": "fa fa-navicon",
        "literature.literaryWork": "fa-solid fa-book",
        "guide.guide": "fa-solid fa-circle-exclamation",
    },
    "custom_css": "css/admin.css",
}

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": {
            "items": [
                "heading",
                "|",
                "bold",
                "italic",
                "underline",
                "strikethrough",
                "|",
                "link",
                "bulletedList",
                "numberedList",
                "|",
                "insertTable",
                "blockQuote",
                "imageUpload",
                "|",
                "undo",
                "redo",
            ]
        }
    }
}

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'BA_study_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'guide.context_processors.admin_guide',
                "django.template.context_processors.i18n",
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'BA_study_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': (
            BASE_DIR / config('DB_NAME', default='db.sqlite3')
            if config('DB_ENGINE', default='django.db.backends.sqlite3') == 'django.db.backends.sqlite3'
            else config('DB_NAME', default='')
        ),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en')

TIME_ZONE = config('TIME_ZONE', default='Asia/Dhaka')

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("bn", "বাংলা"),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOG_VIEWER_FILES = ['app.log', 'error.log']  # add your actual log file names
LOG_VIEWER_FILES_DIR = BASE_DIR / 'logs'  # path to your logs folder
LOG_VIEWER_PAGE_LENGTH = config(
    'LOG_VIEWER_PAGE_LENGTH', default=100, cast=int)

LOG_VIEWER_FORMATS = {
    'bracket_timestamp': {
        'pattern': r'^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\]\s+(?P<level>\w+)\s+(?P<module>\S+)\s+\S+:\d+\s+-\s+(?P<message>.*)$',
        'timestamp_format': '%Y-%m-%d %H:%M:%S,%f',
        'description': 'Bracketed timestamp, level, module, func:line - message',
    }
}

LOG_VIEWER_FILE_FORMATS = {
    'app.log': 'bracket_timestamp',
    'error.log': 'bracket_timestamp',
}

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname:<8} {name} "
                      "{module}.{funcName}:{lineno} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{asctime}] {levelname:<8} {message}",
            "style": "{",
        },
    },

    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "app.log",
            "maxBytes": 5 * 1024 * 1024,   # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
            "delay": True,
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "error.log",
            "maxBytes": 5 * 1024 * 1024,   # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
            "delay": True,
        },
    },

    "root": {
        "handlers": ["file", "error_file"],
        "level": "INFO",
    },

    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
#
X_FRAME_OPTIONS = "SAMEORIGIN"
