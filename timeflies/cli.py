#   encoding: utf8
#   bot.py

import click
import logging

from requests import Session

from .models import connect_database
from .settings import DB_URI
from .telegram import get_updates
from .utils import handle_update


@click.group()
def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)


@main.command(name='loop', help='Use long polling updates handler.')
def main_loop():
    logging.info('run update event loop')

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
