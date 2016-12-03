#!/usr/bin/env python3
#   encoding: utf8
#   utils.py

import logging

from pprint import pprint
from requests import Session
from .settings import *

def send_request(method=None, params=None, sess=None):
    url = API_URL.format(token=API_TOKEN, method=method)
    r = sess.get(url, params=params)
    
    if r.status_code != 200:
        logging.error('request failed with status code %d', r.status_code)
        return None

    content_type = r.headers.get('Content-Type', '')

    if not content_type.startswith('application/json'):
        logging.error('wrong content-type: %s', content_type)
        return None

    try:
        json = r.json()
    except ValueError:
        logging.error('invalid json: %s', res.text)
        return None
    
    return json


