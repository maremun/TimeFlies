#   encoding: utf8
#   db_interaction.py


import logging

from .models import Timelapse, User


def add_user(user_info, database): 
    try:
        telegram_id = user_info['id']
        query = database.query(User).filter(User.id == telegram_id)
        if query.count():
            raise Exception('User already in database (id %d)', telegram_id)
        
        username = user_info['username']
        first_name = user_info['first_name']
        last_name = user_info['last_name']

        user = User(username=username, id=telegram_id, first_name=first_name,
                    last_name=last_name)

        database.add(user)
        database.commit()
        logging.info('user %s added', first_name)

    except Exception as e:
        logging.error('Exception caught: %s', e)


def add_timelapse(timelapse_info, user_id, database):
    try:
        timelapse = Timelapse(user_id=user_id, timelapse_name=timelapse_info)
        database.add(timelapse)
        database.commit()
        logging.info('timelapse %s added for user %d',
                     timelapse_info, user_id)

        # TODO create buttons for editing timelapse settings: units, duration,
        #      description, start_time, progress
    except Exception as e:
        logging.error('Exception caught: %s', e)


