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
    add = 'add'
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


def get_user_info(message):
    user_info = {}
    from_info = message.get('from')
    user_info['id'] = from_info.get('id')
    user_info['first_name'] = from_info.get('first_name')
    user_info['last_name'] = from_info.get('last_name')
    user_info['username'] = from_info.get('username')
    return user_info


def add_user(user_info, database): 
    try:
        telegram_id = user_info['id']
        query = database.query(User).filter(User.id == telegram_id)
        if query.count():
            raise Exception('User already in database (id %d)' % telegram_id)
        
        username = user_info['username']
        first_name = user_info['first_name']
        last_name = user_info['last_name']

        user = User(username=username, id=telegram_id, first_name=first_name, \
                last_name=last_name)
        database.add(user)
        database.commit()
        logging.info('user %s added' % first_name)
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


def get_timelapse_info(message):
    pattern = re.compile(r'/%s (\w+(\s\w+){0,2})' % Command.add.name)
    text = message.get('text')
    match = pattern.search(text)
    timelapse_name = match.group(1)
    return timelapse_name


def add_timelapse(timelapse_info, user_id, database):
    try:
        timelapse = Timelapse(user_id=user_id, timelapse_name=timelapse_info)
        database.add(timelapse)
        database.commit()
        logging.info('timelapse %s added for user %d' % \
                (timelapse_info,user_id))
        # TODO create buttons for editing timelapse settings: units, duration, \
        #      description, start_time, progress 
    except Exception as e:
        logging.error('Exception caught: %s' % e)


def handle_commands(commands, message, database):
    # TODO handle other commands
    user_info = get_user_info(message)

    for c in commands:
        if c==Command.start.name:
            add_user(user_info, database)
        if c==Command.add.name:
            timelapse_info = get_timelapse_info(message)
            user_id = user_info['id']
            add_timelapse(timelapse_info, user_id, database)

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
