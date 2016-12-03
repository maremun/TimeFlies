#   encoding: utf8
#   settings.py

DEBUG = True
API_TOKEN = None
API_URL = 'https://api.telegram.org/bot{token}/{method}'

# override default settings
try:
    from .timeflies_settings import *
except ImportError:
    pass
