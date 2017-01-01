#   encoding: utf8
#   settings.py

from os.path import dirname, join, realpath


# Debug and profiling settings
DEBUG = True
PROFILE = False

# Telegram API credentials
API_TOKEN = None
API_URL = 'https://api.telegram.org/bot{token}/{method}'

# Database settings
DB_URI = 'postgresql+psycopg2:///timelapse'

# override default settings(ignore F401 and F403 flake8 errors)
try:
    from timeflies_settings import API_TOKEN
except ImportError:
    pass
