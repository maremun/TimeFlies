#   encoding: utf8
#   command_handlers.py
"""Defines handlers for bot_commands."""

import logging

from json import loads

from .db_interaction import add_timelapse, add_user, edit_timelapse
from .interaction_utils import UNITS_KEYBOARD, TIMELAPSE_EDIT_KEYBOARD, \
    create_reply_markup
from .models import UnitEnum
from .telegram import answer_callback_query, edit_message_text, send_message


def on_units_button(chat_id, message_id, database, timelapse_id, **kwargs):
    # TODO: Keyboards is not for state storing but for state params sharing!
    if 'set' in kwargs and kwargs['set'] in UNITS_KEYBOARD:
        for unit in UnitEnum:
            if unit.value == kwargs['set']:
                text = 'Got it. Your timelapse countdown is in %s.' \
                        % unit.value

                edit_timelapse(timelapse_id, 'units', unit, database)
                edit_message_text(chat_id, message_id, text)
    else:
        text = 'Please specify units to measure your timelapse ' \
               'progress in'
        payload = dict(func='units')
        keyboard = create_reply_markup(UNITS_KEYBOARD, timelapse_id, **payload)
        edit_message_text(chat_id, message_id, text, reply_markup=keyboard)


def on_duration_button(timelapse_id, chat_id, message_id, database):
    pass


def on_start_time_button(timelapse_id, chat_id, message_id, database):
    pass


def on_progress_button(timelapse_id, chat_id, message_id, database):
    pass


CALLBACK_HANDLERS = {
    'units': on_units_button,
    'duration': on_duration_button,
    'start time': on_start_time_button,
    'progress': on_progress_button,
}


def on_query_update_message(callback_data, query, database):
    try:
        data = loads(callback_data)
    except ValueError:
        return

    handler = data['func']

    if handler in CALLBACK_HANDLERS:
        message = query.get('message')
        chat_id = message.get('chat').get('id')
        message_id = message.get('message_id')

        CALLBACK_HANDLERS[handler](chat_id, message_id, database, **data)


def handle_callback_query(callback_query, database):
    callback_query_id = callback_query.get('id')
    answer_callback_query(callback_query_id)

    callback_data = callback_query.get('data')
    on_query_update_message(callback_data, callback_query, database)


def handle_start(message, database):
    user_info = get_user_info(message)
    chat_id = message.get('chat').get('id')

    first_name = add_user(user_info, database)
    if first_name:
        text = 'Welcome %s!' % first_name
    else:
        text = 'Welcome back %s!' % user_info['first_name']
    return send_message(chat_id, text)


def handle_add(message, database):
    chat_id = message.get('chat').get('id')
    user_id = message.get('from').get('id')
    timelapse_info = get_timelapse_info(message)

    if timelapse_info:
        timelapse_id = add_timelapse(timelapse_info, user_id, database)
        text = "Yay! Your timelapse '%s' has been created! Perhaps you want" \
               "to tweak it a bit?" % timelapse_info
        keyboard = create_reply_markup(TIMELAPSE_EDIT_KEYBOARD, timelapse_id)
        send_message(chat_id, text, reply_markup=keyboard)
    else:
        logging.error('Poor user input. User %d', chat_id)
        text = 'Please provide a name for your brand new timelapse ' \
               '(up to 3 words). Example:\n' \
               '/add MY BEST SUMMER'
        send_message(chat_id, text)

    return timelapse_info


def handle_command(command, message, database):
    for command_name, command_handler in COMMAND_HANDLERS.items():
        if command_name == command:
            command_handler(message, database)


def handle_commands(commands, message, database):
    for command in commands:
        handle_command(command, message, database)


# FIXME; fix cycle dependencies due to wrong module isolation.
from .update_parser import COMMAND_HANDLERS, get_timelapse_info, get_user_info
