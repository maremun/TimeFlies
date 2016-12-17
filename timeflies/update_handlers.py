#   encoding: utf8
#   command_handlers.py
"""Defines handlers for bot_commands."""

import logging

from .db_interaction import add_timelapse, add_user, edit_timelapse
from .interaction_utils import UNITS_KEYBOARD, create_reply_markup, \
        send_keyboard
from .models import UnitEnum
from .telegram import answer_callback_query, edit_message_text, send_message


def on_units_button(timelapse_id, chat_id, message_id, database):
    new_text = 'Please specify units to measure your timelapse ' \
                'progress in'

    new_reply_markup = create_reply_markup(UNITS_KEYBOARD, timelapse_id)
    edit_message_text(chat_id, message_id, new_text, new_reply_markup)


def on_duration_button(timelapse_id, chat_id, message_id, database):
    pass


def on_start_time_button(timelapse_id, chat_id, message_id, database):
    pass


def on_progress_button(timelapse_id, chat_id, message_id, database):
    pass


def on_units_keyboard_button(unit, timelapse_id, chat_id,
                             message_id, database):
    new_text = 'Got it. Your timelapse countdown is in %s.' % unit.value

    edit_timelapse(timelapse_id, 'units', unit, database)
    edit_message_text(chat_id, message_id, new_text)


def on_hours_button(timelapse_id, chat_id, message_id, database):
    return on_units_keyboard_button(UnitEnum.h, timelapse_id,
                                    chat_id, message_id, database)


def on_days_button(timelapse_id, chat_id, message_id, database):
    return on_units_keyboard_button(UnitEnum.d, timelapse_id,
                                    chat_id, message_id, database)


def on_weeks_button(timelapse_id, chat_id, message_id, database):
    return on_units_keyboard_button(UnitEnum.w, timelapse_id,
                                    chat_id, message_id, database)


def on_months_button(timelapse_id, chat_id, message_id, database):
    return on_units_keyboard_button(UnitEnum.m, timelapse_id,
                                    chat_id, message_id, database)


def on_years_button(timelapse_id, chat_id, message_id, database):
    return on_units_keyboard_button(UnitEnum.y, timelapse_id,
                                    chat_id, message_id, database)


# def on_units_keyboard_button(data, timelapse_id, database):
    # TODO think of a way to use something like this...
    # to avoid multiple almost identical functions and
    # also ifelse blocks in on_query_updte_message
#    new_text = 'Got it. Your timelapse countdown is in %s.' % data

#    edit_timelapse(timelapse_id, 'units', data, database)
#    return lambda chat_id, message_id: edit_message_text(
#            chat_id, message_id, new_text)


def on_query_update_message(data, query, database):
    # TODO move separator to top as DATA_SEPARATOR

    data, timelapse_id = data.split('|')

    switch_on_data = {
            'units': on_units_button,
            'duration': on_duration_button,
            'start time': on_start_time_button,
            'progress': on_progress_button,
            'hours': on_hours_button,
            'days': on_days_button,
            'weeks': on_weeks_button,
            'months': on_months_button,
            'years': on_years_button,
    }

    handle_query = switch_on_data.get(data)
    if handle_query:
        message = query.get('message')
        chat_id = message.get('chat').get('id')
        message_id = message.get('message_id')

        handle_query(timelapse_id, chat_id, message_id, database)


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
        send_keyboard(chat_id, timelapse_info, timelapse_id)
    else:
        logging.error('Poor user input. User %d', chat_id)
        text = 'Please provide a name for your brand new timelapse ' \
            '(up to 3 words). Example: \n /add MY BEST SUMMER'
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
