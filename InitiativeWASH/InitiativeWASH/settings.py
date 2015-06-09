# Django settings for InitiativeWASH project.

import os
# import djcelery
# djcelery.setup_loader()
# BROKEN_URL = 'django://'

#DATABASE ROUTER
# RAPIDSMS_ROUTER = "rapidsms.router.db.DatabaseRouter"
##############

# The top directory for this project. Contains requirements/, manage.py,
# and README.rst, a InitiativeWASH directory with settings etc (see
# PROJECT_PATH), as well as a directory for each Django app added to this
# project.
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# The directory with this project's templates, settings, urls, static dir,
# wsgi.py, fixtures, etc.
PROJECT_PATH = os.path.join(PROJECT_ROOT, 'InitiativeWASH')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'InitiativeWASH.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/public/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/public/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files to collect
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'vhi)ty9@61rmo7h$yv8m5o!uuf!op4j2=oxinf&)b&p0#5kz8f'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'InitiativeWASH.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'InitiativeWASH.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)

# A sample logging configuration.
# This logs all rapidsms messages to the file `rapidsms.log`
# in the project directory.  It also sends an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'basic',
            'filename': os.path.join(PROJECT_PATH, 'rapidsms.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'rapidsms': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # External apps
    "django_nose",
    #"djtables",  # required by rapidsms.contrib.locations
    "django_tables2",
    "selectable",
    "south",
    # Project apps
    "gateway",
    # RapidSMS
    "rapidsms",
    "rapidsms.backends.database",
    "rapidsms.contrib.handlers",
    "rapidsms.contrib.httptester",
    "rapidsms.contrib.messagelog",
    "rapidsms.contrib.messaging",
    "rapidsms.contrib.registration",
#    "rapidsms.contrib.echo",
    #INSTALLS THE FOLLOWING
    #Celery and djcelery
    # "djcelery",
    # "kombu.transport.django",
    # "rapidsms.router.celery",
    #DatabaseRouter
    # "rapidsms.router.db",
    #DIRECTORY GATEWAY
    "gateway",
    #TROPO
    # 'rtropo',
    #TWILIO
    "rtwilio",
    #########
    "rapidsms.contrib.default",  # Must be last
)

INSTALLED_BACKENDS = {
    "message_tester": {
        "ENGINE": "rapidsms.backends.database.DatabaseBackend",
        # "router.celery.eager": True,
    },
    # # "twilio-backend": {
    # #     "ENGINE": "rtwilio.outgoing.TwilioBackend",
    # #     'config': {
    # #         'account_sid': 'AC8155be9cc294a5aebd5737e7e87058e0',  # (required)
    # #         'auth_token': '7476383ef820d9cbaada64b495435131',  # (required)
    # #         'number': '(323) 909-4972',  # your Twilio phone number (required)
    # #         # 'callback': 'http://herrickc.scripts.mit.edu/wash/backend/twilio/status-callback/',  # optional callback URL
    # #         # +13239094972
    # #     }
    # },

    "telerivet": {
      "ENGINE": "rapidsms_telerivet.outgoing.TelerivetBackend",
      "project_id": "PJ7857fe403c2fa575",
      "phone_id": "PNcc002e02c198bd4f",
      "secret": "9FT4PNWCMUZ7ZCRA96EPLKZW3ZPZFDFP",
      "api_key": "FTntIwlTyAJKmBJVVqp5XVFbrMMGaUIn"
  },

    # "my-tropo-backend": {
    #     "ENGINE": "rtropo.outgoing.TropoBackend",
    #     'config': {
    #         # Your Tropo application's outbound token for messaging
    #         'messaging_token': '07d15cd1cbb0ba47a68f05b57f43358be8d9e9c4efe70c368b09e16719fba8c58fa1b15561a3f5f44feb6793',
    #         # Your Tropo application's voice/messaging phone number (including country code)
    #         'number': '+1-857-239-0091',
    #     },
    # },
}

###########LOGGING################
# LOGGING_CONFIG = {
#     "rapidsms.router.celery":{
#         'handlers':['file'],
#         'level': DEBUG,
#     }
# }
###################################



LOGIN_REDIRECT_URL = '/'

RAPIDSMS_HANDLERS = (
    'gateway.handlers.DataHandler',
    'gateway.handlers.NeighborhoodHandler',
)

DEFAULT_RESPONSE = "Sorry, we didn't understand your message. Please try again."
