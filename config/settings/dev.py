from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nk#ih)z*+w2eyzee5iqzltcsnock(gucw#*s105+w(vc!938i$'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# WAGTAILAPI_BASE_URL = 'localhost:8000'

RENDER_SERVER_BASE_URL = 'localhost:3001'

REACT = {
    'RENDER': True,
    'RENDER_URL': 'http://127.0.0.1:9009/render',
}

try:
    from .local import *
except ImportError:
    pass
