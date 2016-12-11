#!/usr/bin/env python3
#   encoding: utf8
#   utils.py

import logging
import re
from enum import Enum


from pprint import pprint
from requests import Session

from .settings import *
from .models import User, Timelapse


class Command(Enum):
    # TODO add other commands
    start = 'start'

command_patterns = {c:re.compile('/%s' % c.name) for c in Command}


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
    try:
        telegram_id = user_info.get('id')
        query = database.query(User).filter(User.id == telegram_id)
        if query.count():
            raise Exception('User already in database (id %d)' % telegram_id)
        
        username = user_info.get('username')
        first_name = user_info.get('first_name')
        
        user = User(username=username, id=telegram_id, first_name=first_name)
        database.add(user)
        database.commit()
        logging.info('user %s added' % username)
    except Exception as e:
        logging.error('Exception caught: %s' % e)


def detect_commands(message):
    # TODO should parse all command types and return a list of commands (in case
    # message contains more than one). 

    f = False
    commands = []
    entities = message.get('entities',[])
    text = message.get('text')
    for e in entities:
        if e.get('type') == 'bot_command':
            f = True
            break
    if f:
        for c,p in command_patterns.items():
            if p.search(text):
                commands.append(c.name)
    logging.info('received commands: %s' % commands)
    return commands


def handle_commands(commands, message, database):
    # TODO handle other commands
    
    user_info = message.get('from')
    for c in commands:
        if c==Command.start.name:
            add_user(user_info, database)


def handle_update(update, session, database):
    # TODO account for other types of updates!

    pprint(update)
    message = update.get('message')
    if message:
        commands = detect_commands(message)
        handle_commands(commands, message, database)

    return echo(update, session)


def echo(update, sess):
    m = update.get('message')
    
    if m:
        chat_id = m.get('chat').get('id')
        username = m.get('from').get('username')
        message_text = m.get('text')
        
        text = '%s said %s' % (username, message_text)
        send_message(chat_id, text, sess)
        logging.info(update.get('update_id'))
        return update.get('update_id')
    return 0
