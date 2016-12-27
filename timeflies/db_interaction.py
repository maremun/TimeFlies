#   encoding: utf8
#   db_interaction.py


import logging

from .models import Timelapse, User

# TODO introduce get user/timelapse functions,
# to use get/set the correspoding fields without passing argument database?
# is it better? why?


def add(instance, database):
    database.add(instance)
    database.commit()
    logging.info('%r added', instance)


def add_user(user_info, database):
    try:
        telegram_id = user_info['id']
        query = database.query(User).filter(User.id == telegram_id)
        if query.count():
            raise Exception('User already in database (id %d)' % telegram_id)

        username = user_info['username']
        first_name = user_info['first_name']
        last_name = user_info['last_name']

        user = User(username=username, id=telegram_id, first_name=first_name,
                    last_name=last_name)

        add(user, database)
        return first_name

    except Exception as e:
        logging.error('Exception caught: %s', e)
        return None


def set_state(user_id, state, timelapse_id, database):
    try:
        query = database.query(User).filter(User.id == user_id)
        user = query.one()
        user.state = ''.join([state, '|', str(timelapse_id)])

    except Exception as e:
        logging.error('Exception caught: %s', e)
        return 0


def add_timelapse(title, user_id, database):
    try:
        timelapse = Timelapse(user_id=user_id, title=title)
        add(timelapse, database)
        state = 'add'
        set_state(user_id, state, timelapse.id, database)
        return timelapse.id

    except Exception as e:
        logging.error('Exception caught: %s', e)
        return None


def edit_timelapse_title(timelapse, value):
    timelapse.title = value

    return timelapse


def edit_timelapse_units(timelapse, value):
    timelapse.units = value

    return timelapse


def edit_timelapse_duration(timelapse, value):
    timelapse.duration = value

    return timelapse


def edit_timelapse_start_time(timelapse, value):
    timelapse.start_time = value

    return timelapse


def edit_timelapse_description(timelapse, value):
    timelapse.description = value

    return timelapse


def edit_timelapse(timelapse_id, field, value, database):
    try:
        query = database.query(Timelapse).filter(Timelapse.id == timelapse_id)
        timelapse = query.one()

        switch_on_field = {
                'title': edit_timelapse_title,
                'units': edit_timelapse_units,
                'duration': edit_timelapse_duration,
                'start_time': edit_timelapse_start_time,
                'description': edit_timelapse_description,
        }

        edit_func = switch_on_field.get(field)
        if edit_func:
            edit_func(timelapse, value)

        database.commit()
        logging.info('Timelapse updated: %r.', timelapse)

        return edit_func

    except Exception as e:
        logging.error('Exception caught: %s', e)
        return 0

# TODO handle exceptions!
def get_state(user_id, database):
    try:
        query = database.query(User).filter(User.id == user_id)
        user = query.one()

        return user.state

    except Exception as e:
        logging.info('No such user!')
        logging.error('Exception caught: %s', e)
        return 0


def get_timelapse_by_id(timelapse_id, database):
    try:
        query = database.query(Timelapse).filter(Timelapse.id == timelapse_id)
        timelapse = query.one()

        return timelapse

    except Exception as e:
        logging.error('Exception caught: %s', e)
        return 0
