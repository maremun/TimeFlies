#   encoding: utf8
#  interaction_utils.py

from json import dumps

from .telegram import send_message


TIMELAPSE_EDIT_KEYBOARD = ['units', 'duration', 'start_time', 'progress']
UNITS_KEYBOARD = ['hours', 'days', 'weeks', 'months', 'years']


def make_inline_button(text, callback_data=' ', timelapse_id=None):
    callback_data = '%s|%s' % (text, timelapse_id)
    
    return dict(text=text, callback_data=callback_data)


def create_reply_markup(keys, timelapse_id=None):
    # TODO rewrite to use **kwargs? in case we would like 
    # to share not only timelapse id.
    keyboard = [[make_inline_button(key, timelapse_id=timelapse_id) 
        for key in keys]]

    reply_markup = dict(inline_keyboard=keyboard)
    return dumps(reply_markup)


def send_keyboard(chat_id, timelapse_info, timelapse_id):
    # TODO session?
    text = 'Yay! Your timelapse \'%s\' has been created! Perhaps you want to ' \
            'tweak it a bit?' % timelapse_info
    
    reply_markup = create_reply_markup(TIMELAPSE_EDIT_KEYBOARD, timelapse_id)
    send_message(chat_id, text, reply_markup=reply_markup)


