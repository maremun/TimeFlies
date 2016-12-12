#   encoding: utf8
#   settings.py

from os.path import dirname, join, realpath

root = realpath(join(dirname(__file__), '..'))
path_to_database = join(root, 'var/timeflies.db')

# Debug and profiling settings
DEBUG = True
PROFILE = False

# Telegram API credentials
API_TOKEN = None
API_URL = 'https://api.telegram.org/bot{token}/{method}'

# Database settings
DB_URI = 'sqlite:///%s' % path_to_database

# override default settings(ignore F401 and F403 flake8 errors)
try:
    from timeflies_settings import *
except ImportError:
    pass
