#   encoding: utf8
#   interaction_utils.py

from json import dumps


TIMELAPSE_EDIT_KEYBOARD = ['title', 'units', 'duration', 'start time',
                           'description', 'add note', 'delete']
UNITS_KEYBOARD = ['hours', 'days', 'weeks', 'months', 'years']


def make_inline_button(text, **kwargs):
    callback_data = dict(set=text, func=text)
    callback_data.update(kwargs)
    return dict(text=text, callback_data=dumps(callback_data))


def create_reply_markup(keys, **kwargs):
    keyboard = [[make_inline_button(key, **kwargs)
                for key in keys]]
    keyboard[0].append(make_inline_button('back', **dict(func='back')))
    keyboard = [keyboard[0][i-2:i] for i in range(2,len(keyboard[0])+2,2)]
    reply_markup = dict(inline_keyboard=keyboard)
    return dumps(reply_markup)
