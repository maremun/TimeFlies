#!/usr/bin/env python3
#   encoding: utf8
#   bot.py

import click
import logging

from pprint import pprint
from requests import Session

from .models import connect_database
from .settings import *
from .utils import send_request, handle_update


def get_updates(offset=None, limit=100, timeout=60, sess=None):
    params = dict(offset=offset, limit=limit, timeout=60)
    return send_request('getUpdates', params, sess)


def update_loop():
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


@click.group()
def main():
    logging.basicConfig(level=logging.INFO)


@main.command(name='loop')
def main_loop():
    update_loop()


if __name__ == '__main__':
    main()
