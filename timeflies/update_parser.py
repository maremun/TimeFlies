#   encoding: utf8
#   update_parser.py

import logging
import re

from datetime import datetime

from .db_interaction import get_state


def get_timelapse_title(message):
    try:
        pattern = re.compile(r'/add (\w+(\s\w+){0,2})')
        text = message.get('text')
        match = pattern.search(text)
        timelapse_name = match.group(1)
        return timelapse_name
    except AttributeError:
        logging.error('No timelapse name')


def get_user_info(message):
    user_info = {}
    from_info = message.get('from')
    user_info['id'] = from_info.get('id')
    user_info['first_name'] = from_info.get('first_name')
    user_info['last_name'] = from_info.get('last_name')
    user_info['username'] = from_info.get('username')
    return user_info


def parse_query(query, database):
    try:
        message = query.get('message')
        chat_id = message.get('chat').get('id')
        message_id = message.get('message_id')
        
        return chat_id, message_id

    except Exception as e:
        logging.error('Exception caught: %s', e)
        return None


def parse_for_state(upd, database):
    try:
        user_id = upd.get('from').get('id')
        state_string = get_state(user_id, database) 
        logging.info(state_string)
        if state_string:
            state, timelapse_id = state_string.split('|')
            timelapse_id = int(timelapse_id)

        # TODO resolve new comers better
        else:
            state = 'start'
            timelapse_id = -1
        
        return state, timelapse_id, user_id

    except Exception as e:
        logging.error('Exception caught: %s', e)
        return None


def parse_date(text):
    try:
        dt = datetime.strptime(text, '%m/%d/%Y')
        return dt

    except Exception as e:
        logging.error('Exception caught: %s', e)
        return None
