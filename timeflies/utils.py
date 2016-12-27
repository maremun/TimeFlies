#   encoding: utf8
#   utils.py

from pprint import pprint

from .update_handlers import handle_callback_query, \
        handle_message, not_supported


def handle_update(update, session, database):
    pprint(update)
    message = update.get('message')
    callback_query = update.get('callback_query')

    if message:
        handle_message(message, database)
    if callback_query:
        handle_callback_query(callback_query, database)
    else:
        not_supported(update)

    return update.get('update_id')
