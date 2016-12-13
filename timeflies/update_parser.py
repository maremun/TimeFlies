#   encoding: utf8
#   update_parser.py


import logging
import re

from enum import Enum
from pprint import pprint


class Command(Enum):
    # TODO add other commands
    start = 'start'
    add = 'add'
    
command_patterns = {c: re.compile('/%s' % c.name) for c in Command}


def get_user_info(message):
    user_info = {}
    from_info = message.get('from')
    user_info['id'] = from_info.get('id')
    user_info['first_name'] = from_info.get('first_name')
    user_info['last_name'] = from_info.get('last_name')
    user_info['username'] = from_info.get('username')
    return user_info


def detect_commands(message):
    # TODO should parse all command types and return a list of commands (in
    # case message contains more than one).

    f = False
    commands = []
    entities = message.get('entities', [])
    text = message.get('text')
    for e in entities:
        if e.get('type') == 'bot_command':
            f = True
            break
    if f:
        for c, p in command_patterns.items():
            if p.search(text):
                commands.append(c.name)
    logging.info('received commands: %s', commands)
    return commands


def get_timelapse_info(message):
    try:
        pattern = re.compile(r'/%s (\w+(\s\w+){0,2})' % Command.add.name)
        text = message.get('text')
        match = pattern.search(text)
        timelapse_name = match.group(1)
        return timelapse_name
    except AttributeError:
        logging.error('No timelapse name')



