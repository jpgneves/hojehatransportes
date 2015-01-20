# Django settings for hojehatransportes project.
import os
from social_auth_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'hagreve', # Or path to database file if using sqlite3.
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'ahp0ise!'

#		'ENGINE': 'django_mongodb_engine', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#		'NAME': 'hagreve', # Or path to database file if using sqlite3.
    }
}

#Root URL for Static files
#STATIC_URL = 'http://localhost/~carlos/hagreve/hojehatransportes/static'
STATIC_URL = 'https://static.hagreve.com/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Lisbon'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-PT'

SITE_ID=1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

DATETIME_INPUT_FORMATS=('%Y/%m/%d %H:%M:%S',  '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M', '%m/%d/%Y','%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M', '%m/%d/%y')

#DATETIME_FORMAT=('%Y-%m-%d %H:%M:%S')


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://static.hagreve.com/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'yrn2@+zm$ww8avsi^)0=2x-6hx@osq0_a3qx7jx&o%)alm_#op'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'hojehatransportes.hat.middleware.MultipleProxyMiddleware',
)

ROOT_URLCONF = 'hojehatransportes.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/hojehatransportes/templates" % os.getcwd()
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "hojehatransportes.settings.static_url_processor",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'hojehatransportes.hat',
    'social_auth'#,
    #'django_mongodb_engine'
)

# Auth

SOCIAL_AUTH_IMPORT_BACKENDS = (
    'social_auth_extra',
)

AUTHENTICATION_BACKENDS = (
    # 'social_auth.backends.twitter.TwitterBackend',
    # 'social_auth.backends.facebook.FacebookBackend',
    # 'social_auth.backends.google.GoogleBackend',
    # 'social_auth_extra.sapo.SapoBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Additional user data

AUTH_PROFILE_MODEL = "hat.UserProfile"


########## Add setting to thre request
def static_url_processor(request):
    my_dict = {
        'static_url': STATIC_URL,
    }
    return my_dict

