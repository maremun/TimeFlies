#   encoding: utf8
#   command_handlers.py
"""Defines handlers for bot_commands."""

import logging 

from .db_interaction import add_timelapse, add_user
from .interaction_utils import send_keyboard 
from .telegram import send_message
from .update_parser import Command, get_timelapse_info, get_user_info

def handle_commands(commands, message, database):
    # TODO handle other commands
    user_info = get_user_info(message)
    chat_id = message.get('chat').get('id')
    
    for c in commands:
        if c == Command.start.name:
            add_user(user_info, database)
            continue
        if c == Command.add.name:
            timelapse_info = get_timelapse_info(message)
            if timelapse_info:
                user_id = user_info['id']
                add_timelapse(timelapse_info, user_id, database)
                send_keyboard(chat_id, timelapse_info)
            else: 
                # TODO create handle_input_problem(problem) which will decide on
                # an Exception and send a corresponding message to user stating 
                # the problem in the input. Also send a template for a command?
                logging.error('Poor user input. User %d', chat_id)
                text = 'Please provide a name for timelapse (up to 3 words).'
                send_message(chat_id, text)
            continue



