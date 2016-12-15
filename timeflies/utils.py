#   encoding: utf8
#   utils.py

from pprint import pprint

from .update_handlers import handle_callback_query, handle_commands
from .telegram import send_message
from .update_parser import detect_commands


def handle_update(update, session, database):
    # TODO account for other types of updates!

    pprint(update)
    message = update.get('message')
    callback_query = update.get('callback_query')

    if message:
        commands = detect_commands(message)
        handle_commands(commands, message, database)
    if callback_query:
        handle_callback_query(callback_query, database)

    return update.get('update_id')
    # return echo(update, session)


def echo(update, sess):
    m = update.get('message')

    if m:
        chat_id = m.get('chat').get('id')
        username = m.get('from').get('username')
        message_text = m.get('text')

        text = '%s said %s' % (username, message_text)
        send_message(chat_id, text, sess=sess)

    return update.get('update_id')
