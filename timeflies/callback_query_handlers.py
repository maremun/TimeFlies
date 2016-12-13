#   encoding: utf8
#   callback_query_handlers.py
"""Defines handlers for callback queries. Timelapse editing involves inline 
keyboards that generate callbacks that should be answered with appropriate 
action."""


import logging

from .telegram import answer_callback_query, edit_message_text
from .interaction_utils import UNITS_KEYBOARD, create_reply_markup

def handle_callback_query(callback_query):
    # TODO generalize this function, move timelapse editing out to
    # e.g. timelapse_edit()

    callback_query_id = callback_query.get('id')
    answer_callback_query(callback_query_id)

    data = callback_query.get('data')
    message = callback_query.get('message')
    chat_id = message.get('chat').get('id')
    message_id = message.get('message_id')
    
    new_text = 'Please specify %s to measure your timelapse progress in' % data
    if data == 'units':
        new_reply_markup = create_reply_markup(UNITS_KEYBOARD)
        edit_message_text(chat_id, message_id, new_text, new_reply_markup)
    else:
        pass


