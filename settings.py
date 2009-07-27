import os
import django
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
PROD = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Benjamin Kreeger', 'benjaminkreeger@missouristate.edu'),
)

MANAGERS = ADMINS

# When dumping data, --exclude=auth --exclude=contenttypes
if PROD == False:
	DATABASE_ENGINE = 'postgresql_psycopg2'
	DATABASE_NAME = 'etcetera'
	DATABASE_USER = 'etcetera'
	DATABASE_PASSWORD = 'etcetera'
	DATABASE_HOST = 'localhost'
	DATABASE_PORT = ''
else:
	DATABASE_ENGINE = 'postgresql_psycopg2'
	DATABASE_NAME = 'etcetera'
	DATABASE_USER = 'etcetera'
	DATABASE_PASSWORD = 'etcetera'
	DATABASE_HOST = 'localhost'
	DATABASE_PORT = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wy39_df!ur^y(ve8ytxii@4xaewg$19g63$^u@8u5dfs2$!iv7'

# List of callables that know how to import templates from various sources.
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
	'etcetera.repair',
	'etcetera.mlab',
	#'etcetera.reports',
	'etcetera.structure',
	'etcetera.extras',
)
