from .base import *

# Development-specific settings
DEBUG = True

# Local dev convenience: allow localhost hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Development-specific email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
