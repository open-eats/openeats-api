# Django settings for openeats project.
import os, datetime

# We can't set the debug just using the env var.
# Python with evaluate any string as a True bool.
DEBUG = False
if os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true':
    DEBUG = True

SERVE_MEDIA = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'ChangeMe!')

# Force Django to use https headers if its behind a https proxy.
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#secure-proxy-ssl-header
if os.environ.get('HTTP_X_FORWARDED_PROTO', 'False').lower() == 'true':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.environ.get('MYSQL_DATABASE', 'openeats'),
        'USER': os.environ.get('MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD', ''),
        'HOST': os.environ.get('MYSQL_HOST', 'db'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
        'TEST': {
            'NAME': os.environ.get('MYSQL_TEST_DATABASE', 'test_openeats')
        }
    }
}
if 'django.db.backends.mysql' in DATABASES['default']['ENGINE']:
    DATABASES['default'].setdefault('OPTIONS', {})
    DATABASES['default']['OPTIONS']['charset'] = 'utf8mb4'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'node', 'web']

env_allowed_host = os.environ.get('ALLOWED_HOST', None)
if env_allowed_host is not None:
    if ',' in env_allowed_host:
        ALLOWED_HOSTS += [host.strip() for host in env_allowed_host.split(',')]
    else:
        ALLOWED_HOSTS.append(env_allowed_host)

# List of callables that know how to import templates from various sources.
TEMPLATES = [
    {
        'NAME': 'Core Templates',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, 'templates'), ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        'NAME': '3rd Party Templates',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'coreapi',

    'base',
    'v1.recipe',
    'v1.recipe_groups',
    'v1.ingredient',
    'v1.news',
    'v1.list',
    'v1.menu',
    'v1.rating',

    'imagekit',
    'django_extensions',
    'corsheaders'
)

# Password validation
# https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#password-validation
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

ROOT_URLCONF = 'base.urls'

WSGI_APPLICATION = 'base.wsgi.application'

# Automatically find the correct time zone to use.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
    }
}

# http://getblimp.github.io/django-rest-framework-jwt/#additional-settings
JWT_AUTH = {
    # We are returning custom data to our UI.
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'v1.accounts.jwt_handler.handler',

    # Allow for token refresh and increase the timeout of the user token.
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=14),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(weeks=30),
}

# We don't want the API to serve static in production.
# So we are forcing the renderer to be JSON only.
if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )

CORS_ORIGIN_WHITELIST = (
    os.environ.get('NODE_URL', 'localhost:8080')
)

# Static and i18n settings
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

LOCALE_PATHS = (
  os.path.join(PROJECT_PATH, 'locale', ),
)

FIXTURE_DIRS = [
    os.path.join(PROJECT_PATH, 'v1', 'fixtures'),
]

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'site-media')
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static-files')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site-media/'
STATIC_URL = '/static-files/'

ugettext = lambda s: s
LANGUAGES = (
     ('en', ugettext('English')),
     ('de', ugettext('German')),
   )

try:
    from local_settings import *
except ImportError:
    pass
