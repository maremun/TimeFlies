#   encoding: utf8
#   settings.py

DEBUG = True

try:
    from timeflies_settings import *
except ImportError:
    pass
