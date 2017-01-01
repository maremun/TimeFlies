#!/bin/python3
#   encoding: utf8
#   notifications.py

import logging

from .telegram import send_message
from .models import connect_database
from .models import Timelapse, User

def collect_user_ids_to_notify(database):
    # TODO Introduce filtering users to notify 
    # there should be a field in User object specifying 
    # if the user is willing to be notified and if yes how often
    # Currently all are collected
    try:
        query = database.query(User.id)
        return query.all()
    except Exception as e:
        logging.error('Exception caught: %s', e)
        return []


def collect_timelapses(user_id, database):
    try:
        query = database.query(Timelapse).filter(Timelapse.user_id == user_id)
        return query.all()
    except Exception as e:
        logging.error('Exception caught: %s', e)
        return []


def send_notifications(database):
    template = 'Hello there! Is there any progress with your ' \
            'timelapse {:s}?'

    user_ids = collect_user_ids_to_notify(database)
    for u_id in user_ids:
        chat_id = u_id
        timelapses = collect_timelapses(u_id, database)
        for timelapse in timelapses:
            send_message(chat_id, template.format(timelapse.title))
