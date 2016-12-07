#!/usr/bin/env python3
#   encoding: utf8
#   utils.py

import logging

from requests import Session

from .settings import *
from .models import User, Timelapse

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
        logging.error('invalid json: %s', res.text)
        return None
    
    return json


def send_message(chat_id, text, sess=None):
    params = dict(chat_id=chat_id, text=text)
    return send_request('sendMessage', params, sess)


def add_user(user_info, database):
    
    username = user_info.get('username')
    telegram_id = user_info.get('id')
    first_name = user_info.get('first_name')

    user = User(username=username, telegram_id=telegram_id, first_name=first_name)
    database.add(user)
    database.commit()
    logging.info('user %s added' % username)


def handle_update(update, session, database):
    
    user_info = update.get('message').get('from')
    add_user(user_info, database)

    return echo(update, session)


def echo(update, sess):
    m = update.get('message')
    
    if m:
        chat_id = m.get('chat').get('id')
        username = m.get('from').get('username')
        message_text = m.get('text')
        
        text = '%s said %s' % (username, message_text)
        send_message(chat_id, text, sess)
        return update.get('update_id')
    return 0
