#   encoding: utf8
#   settings.py

from os.path import dirname, join, realpath
DEBUG = True
API_TOKEN = None
API_URL = 'https://api.telegram.org/bot{token}/{method}'

root = realpath(join(dirname(__file__), '..'))
path_to_database = join(root, 'var/timeflies.db')
DB_URI = 'sqlite:///%s' % path_to_database

# override default settings
try:
    from .timeflies_settings import *
except ImportError:
    pass
