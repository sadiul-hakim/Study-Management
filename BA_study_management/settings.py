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
    "welcome_sign": "Welcome to Study Management Dashboard",
    "site_icon": "images/fav.png",
    "site_logo": "images/logo.png",
    "login_logo": "images/login_logo.png",
    "show_theme_chooser": False,
    "language_chooser": True,
    "topmenu_links": [
        {"name": "Home Portal", "url": "home", "permissions": ["auth.view_user"], "icon": "fas fa-home"},
        {"name": "Document Viewer", "url": "/admin/viewer", "permissions": ["document.view_document"], "icon": "fas fa-file-alt"},
    ],
    "icons": {
        "auth.user": "fas fa-user-shield",
        "auth.group": "fas fa-users-cog",
        "book_reading.course": "fa-solid fa-graduation-cap",
        "book_reading.book": "fas fa-book-open",
        "book_reading.chapter": "fa-solid fa-bookmark",
        "book_reading.readingProgress": "fa-solid fa-bars-progress",
        "book_reading.otherStudyProgress": "fa-solid fa-list-check",
        "book_reading.readingPlan": "fa-solid fa-fire-flame-curved",
        "book_reading.revise": "fa-solid fa-arrows-rotate",
        "document.document": "fa-solid fa-folder-closed",
        "document.documentfile": "fa-solid fa-file-lines",
        "document.genre": "fa-solid fa-tag",
        "document.link": "fa-solid fa-arrow-up-right-from-square",
        "exam_management.exam": "fa-solid fa-pen-ruler",
        "exam_management.improve": "fa-solid fa-arrow-trend-up",
        "general.notes": "fa-solid fa-sticky-note",
        "general.studyNote": "fa-solid fa-file-pen",
        "general.wordcollection": "fa-solid fa-spell-check",
        "writing_plan.writingPlan": "fa-solid fa-feather",
        "literature.author": "fa-solid fa-feather-pointed",
        "literature.genre": "fa-solid fa-tags",
        "literature.literaryWork": "fa-solid fa-book-journal-whills",
        "guide.guide": "fa-solid fa-circle-info",
        "BookCollection.author": "fa-solid fa-user-pen",
        "BookCollection.genre": "fa-solid fa-layer-group",
        "BookCollection.book": "fa-solid fa-book-bookmark",
        "BookCollection.readingprogress": "fa-solid fa-chart-line",
        "BookCollection.readingplan": "fa-solid fa-calendar-days",
        "BookCollection.studynote": "fa-solid fa-note-sticky",
        "BookCollection.lend": "fa-solid fa-hand-holding-heart",
    },
    "custom_css": "css/admin.css",
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
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
