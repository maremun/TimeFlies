#   encoding: utf8
#   bot.py

import click
import logging

from requests import Session

from .models import connect_database
from .settings import DB_URI
from .telegram import get_me, get_updates, set_webhook
from .utils import handle_update
from .notifications import send_notifications


@click.group()
def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)


@main.command(name='loop', help='Use long polling updates handler.')
def main_loop():
    logging.info('running update event loop')
    sess = Session()
    database = connect_database(DB_URI)
    offset = 0

    while True:
        updates = get_updates(offset=offset, sess=sess)

        if updates is None:
            continue

        for upd in updates.get('result'):
            upd_id = handle_update(upd, sess, database)
            offset = max(offset, upd_id) + 1


@main.command(name='me', help='Show account info.')
def main_me():
    me = get_me()['result']

    logging.info('ACCOUNT INFO:')

    if me:
        logging.info('id:         %s', me.get('id'))
        logging.info('first name: %s', me.get('first_name'))
        logging.info('last name:  %s', me.get('last_name'))
        logging.info('username:   @%s', me.get('username'))
    else:
        logging.info('no account info, probably token is wrong.')


@main.command(name='webhook', help='Set webhook.')
@click.argument('url')
def main_webhook(url):
    logging.info('setting up webhook url `%s`', url)
    set_webhook(url)
    logging.info('done.')


@main.command(name='notify', help='Send notifications.')
def main_notify():
    logging.info('sending notifications.')
    database = connect_database(DB_URI)
 
    send_notifications(database)
    logging.info('done.')
