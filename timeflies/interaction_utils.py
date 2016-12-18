#   encoding: utf8
#   interaction_utils.py

from json import dumps

from .telegram import send_message


TIMELAPSE_EDIT_KEYBOARD = ['units', 'duration', 'start_time', 'progress']
UNITS_KEYBOARD = ['hours', 'days', 'weeks', 'months', 'years']


def make_inline_button(text, timelapse_id=None, **kwargs):
    callback_data = dict(set=text, func=text, timelapse_id=timelapse_id)
    callback_data.update(kwargs)
    return dict(text=text, callback_data=dumps(callback_data))


def create_reply_markup(keys, timelapse_id=None, **kwargs):
    # TODO rewrite to use **kwargs? in case we would like
    # to share not only timelapse id.
    # FIXME: very well! but not store state here!
    keyboard = [[make_inline_button(key, timelapse_id=timelapse_id, **kwargs)
                for key in keys]]

    reply_markup = dict(inline_keyboard=keyboard)
    return dumps(reply_markup)
