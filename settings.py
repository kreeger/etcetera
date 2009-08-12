import os
import django
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# A few flags, first
DEBUG = True
PROD = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Benjamin Kreeger', 'benjaminkreeger@missouristate.edu'),
)

MANAGERS = ADMINS

# Database settings
# When dumping data, --exclude=auth --exclude=contenttypes
if PROD == False:
	DATABASE_ENGINE = 'postgresql_psycopg2'
	DATABASE_NAME = 'etcetera'
	DATABASE_USER = 'etcetera'
	DATABASE_PASSWORD = 'Ch33kyBugg3r!!'
	DATABASE_HOST = 'localhost'
	DATABASE_PORT = ''
else:
	DATABASE_ENGINE = 'postgresql_psycopg2'
	DATABASE_NAME = 'etcetera'
	DATABASE_USER = 'etcetera'
	DATABASE_PASSWORD = 'Ch33kyBugg3r!!'
	DATABASE_HOST = 'localhost'
	DATABASE_PORT = ''

# Locale settings
TIME_ZONE = 'America/Chicago'
DATETIME_FORMAT = 'n.j.Y g:iA'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

# Path settings
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'wy39_df!ur^y(ve8ytxii@4xaewg$19g63$^u@8u5dfs2$!iv7'

# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_ADDRESS = r'educationaltechnologycenter@gmail.com'
EMAIL_HOST_USER = r'educationaltechnologycenter@gmail.com'
EMAIL_HOST_PASSWORD = r'R&negade'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[ETCETERA] '

# Other Django settings
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
ROOT_URLCONF = 'etcetera.urls'
FIXTURE_DIRS =  (
	(os.path.join(SITE_ROOT, 'extras/fixtures')),
)
TEMPLATE_DIRS = (
	(os.path.join(SITE_ROOT, 'templates')),
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
	'django.contrib.admin',
	#'etcetera.checkout',
	'etcetera.equipment',
	'etcetera.service',
	'etcetera.mlab',
	#'etcetera.reports',
	'etcetera.structure',
	'etcetera.extras',
)
