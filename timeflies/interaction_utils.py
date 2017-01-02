#   encoding: utf8
#   interaction_utils.py

from json import dumps


FREQUENCY_KEYBOARD = ['daily', 'weekly', 'monthly']
HOURS_KEYBOARD = ['%2d:00' % i for i in range(24)]
TIMELAPSE_EDIT_KEYBOARD = ['title', 'units', 'duration', 'start time',
                           'description', 'add note', 'set reminder', 'delete']
UNITS_KEYBOARD = ['days', 'weeks', 'months', 'years']

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
