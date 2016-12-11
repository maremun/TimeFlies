#   encoding: utf8
#   telegram.py
"""Define binding for Telegram Bot API. There are defined only the most useful
method. Others are skipped.

See for details https://core.telegram.org/bots/api.
"""

import logging

from requests import Session
from .settings import API_URL, API_TOKEN


def send_request(method=None, params=None, sess=None):
    if not sess:
        sess = Session()

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
        logging.error('invalid json: %s', r.text)
        return None

    return json


def get_updates(offset=None, limit=100, timeout=60, sess=None):
    params = dict(offset=offset, limit=limit, timeout=60)
    return send_request('getUpdates', params, sess)


def send_message(chat_id, text, sess=None):
    params = dict(chat_id=chat_id, text=text)
    return send_request('sendMessage', params, sess)
