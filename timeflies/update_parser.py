#   encoding: utf8
#   update_parser.py

import logging
import re

from .update_handlers import handle_add, handle_start


COMMAND_HANDLERS = dict(
    start=handle_start,
    add=handle_add,
)


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

    commands = []
    entities = message.get('entities', [])
    text = message.get('text')

    for e in entities:
        if e.get('type') != 'bot_command':
            continue

        for command_name in COMMAND_HANDLERS.keys():
            offset = e.get('offset', 0)
            length = e.get('length', 0)

            if text[offset + 1:offset + 1 + length].startswith(command_name):
                commands.append(command_name)

    logging.info('received commands: %s', commands)
    return commands


def get_timelapse_info(message):
    try:
        pattern = re.compile(r'/add (\w+(\s\w+){0,2})')
        text = message.get('text')
        match = pattern.search(text)
        timelapse_name = match.group(1)
        return timelapse_name
    except AttributeError:
        logging.error('No timelapse name')
