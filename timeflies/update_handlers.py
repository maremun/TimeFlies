#   encoding: utf8
#   update_handlers.py
"""Defines handlers for updates."""

import logging

from json import loads
from datetime import datetime, timedelta

from .db_interaction import add_timelapse, add_user, edit_timelapse, \
        set_state, get_timelapse_by_id, get_timelapse_by_title, \
        get_user_timelapses, remove_timelapse, get_notes, add_timelapse_note
from .interaction_utils import FREQUENCY_KEYBOARD, HOURS_KEYBOARD, \
        UNITS_KEYBOARD, TIMELAPSE_EDIT_KEYBOARD, create_reply_markup
from .models import UnitEnum
from .telegram import answer_callback_query, edit_message_text, send_message
from .update_parser import get_timelapse_title, get_user_info, \
        parse_query, parse_for_state, parse_date

# TODO handle Exceptions, e.g. getting text field of a message triggers
# Exception whenever message contains no text (audio, document, game, etc).
# TODO Also catch casting errors!


def to_starting_state(user_id, chat_id, database):
    state = 'start'
    timelapse_id = -1
    set_state(user_id, state, timelapse_id, database)
    text = 'You can now choose to /add *new timelapse*, /track or /edit ' \
            'your timelapses.' 
    send_message(chat_id, text)

# TODO rename query arg since it can be message as well
# OR unite handling message updates and callbackQuery updates
def on_title_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)

    # if true query is actually a message update
    if state == 'title': 
        chat_id = query.get('chat').get('id')
        text = query.get('text')
        
        new_title = text
        old_title = get_timelapse_by_id(timelapse_id, database).title
        edit_timelapse(timelapse_id, 'title', new_title, database)

        text = 'Got it. Old title was %s. New title for the timelapse is %s.' \
            % (old_title, new_title)
        send_message(chat_id, text)

        to_starting_state(user_id, chat_id, database)

    # if false query is indeed a callbackQuery
    else:
        chat_id, message_id = parse_query(query, database)

        text = 'Please specify new awesome title for the timelapse, ' \
                'e.g. Coffee-Free.'
        edit_message_text(chat_id, message_id, text)

        state = 'title'
        set_state(user_id, state, timelapse_id, database)


def on_units_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)

    if state == 'units': 
        chat_id, message_id = parse_query(query, database)

        for unit in UnitEnum:
            if unit.value == kwargs['set']:
                text = 'Got it. Your timelapse countdown is now in %s.' \
                        % unit.value

                edit_timelapse(timelapse_id, 'units', unit, database)
                edit_message_text(chat_id, message_id, text)
                break

        to_starting_state(user_id, chat_id, database)

    else:
        chat_id, message_id = parse_query(query, database)

        text = 'Please specify units to measure your timelapse ' \
               'progress in'
        payload = dict(func='units')
        keyboard = create_reply_markup(UNITS_KEYBOARD, **payload)
        edit_message_text(chat_id, message_id, text, reply_markup=keyboard)

        state = 'units'
        set_state(user_id, state, timelapse_id, database)


def on_duration_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)

    if state == 'duration': 
        chat_id = query.get('chat').get('id')
        text = query.get('text')

        new_duration = int(text)
        timelapse = get_timelapse_by_id(timelapse_id, database)
        old_duration = timelapse.duration
        units = timelapse.units.value
        edit_timelapse(timelapse_id, 'duration', new_duration, database)

        text = 'Got it. Previously your timelapse lasted %d %s. ' \
            'Now it is %d.' \
            % (old_duration, units, new_duration)
        send_message(chat_id, text)

        to_starting_state(user_id, chat_id, database)

    else:
        chat_id, message_id = parse_query(query, database)

        text = 'Please specify new duration for the timelapse as a number.'
        edit_message_text(chat_id, message_id, text)

        state = 'duration'
        set_state(user_id, state, timelapse_id, database)


# TODO calendar from inline keyboard
def on_start_time_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)

    if state == 'start time': 
        chat_id = query.get('chat').get('id')
        text = query.get('text')

        new_date = parse_date(text)

        if new_date:
            edit_timelapse(timelapse_id, 'start time', new_date, database)
            text = 'Got it. Your timelapse start time is %s' \
                    % new_date.strftime('%d %b %Y')
            send_message(chat_id, text)
            to_starting_state(user_id, chat_id, database)
        else:
            text = 'There must have been a misprint in your last input. ' \
                   'I am only a silly bot. Please be kind and specify ' \
                   'the start time in the following format mm/dd/yyyy. ' \
                   'Thank you!'
            send_message(chat_id, text)
    else:
        chat_id, message_id = parse_query(query, database)
        text = 'Please specify new start time for the timelapse as a date ' \
                'in the following format mm/dd/yyyy, e.g. 01/14/2017.'
        edit_message_text(chat_id, message_id, text)

        state = 'start time'
        set_state(user_id, state, timelapse_id, database)


def on_description_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)

    if state == 'description': 
        chat_id = query.get('chat').get('id')
        text = query.get('text')

        timelapse = get_timelapse_by_id(timelapse_id, database)

        # TODO make a check for description contents and size!
        edit_timelapse(timelapse_id, 'description', text, database)
        text = 'Got it. Timelapse %s description updated.' % timelapse.title
        send_message(chat_id, text)
        to_starting_state(user_id, chat_id, database)

    else:
        chat_id, message_id = parse_query(query, database)
        
        text = 'Please specify new description for the timelapse, ' \
                'e.g. Leave without coffee for a week.'
        edit_message_text(chat_id, message_id, text)
        
        state = 'description'
        set_state(user_id, state, timelapse_id, database)


def on_add_note_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)

    if state == 'add note': 
        chat_id = query.get('chat').get('id')
        text = query.get('text')
        
        timelapse = get_timelapse_by_id(timelapse_id, database)

        # TODO check note contents and size!
        add_timelapse_note(timelapse.id, text, database)
        text = 'Got it. Added a new note to the timelapse %s.' \
                % timelapse.title
        send_message(chat_id, text)
        to_starting_state(user_id, chat_id, database)

    else:
        chat_id, message_id = parse_query(query, database)

        text = 'Please add a note to the timelapse, ' \
                'e.g. Easy coffee-free day today!'
        edit_message_text(chat_id, message_id, text)

        state = 'add note'
        set_state(user_id, state, timelapse_id, database)


def on_delete_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)
    timelapse = get_timelapse_by_id(timelapse_id, database)
    chat_id, message_id = parse_query(query, database)

    logging.info(timelapse.title)
    if state == 'delete': 
        if kwargs['set'] == 'Yes':
            remove_timelapse(timelapse_id, database)
            text = 'Timelapse %s successfully deleted!' % timelapse.title
        else:
            text = 'Deletion of timelapse %s canceled' % timelapse.title

        edit_message_text(chat_id, message_id, text)
        to_starting_state(user_id, chat_id, database)

    else:
        text = 'Are you sure you want to delete the timelapse %s?' \
               % timelapse.title
        payload = dict(func='delete')
        keyboard = create_reply_markup(['Yes', 'No'], **payload)
        edit_message_text(chat_id, message_id, text, reply_markup=keyboard)

        state = 'delete'
        set_state(user_id, state, timelapse_id, database)


def on_edit(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)

    if timelapse_id == -1:
        chat_id, message_id = parse_query(query, database)
        # get timelpase_id by timelapse name
        timelapse_id = get_timelapse_by_title(kwargs['set'], database).id

        text = 'Please choose the field you want to edit.'
        keyboard = create_reply_markup(TIMELAPSE_EDIT_KEYBOARD)
        edit_message_text(chat_id, message_id, text, reply_markup=keyboard)
        
        # set state to edit|timelapse_id
        set_state(user_id, state, timelapse_id, database)

    else:
        # TODO after editing one field we want to return user not to starting 
        # state actually, but this should be done after we introduce back 
        # buttons in keyboards
        pass


def on_main_menu_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)
    chat_id, message_id = parse_query(query, database)

    text = 'Roger that, back to main menu!' 
    edit_message_text(chat_id, message_id, text)

    to_starting_state(user_id, chat_id, database)


def on_track(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)

    chat_id, message_id = parse_query(query, database)
    # get timelpase_id by timelapse title
    timelapse = get_timelapse_by_title(kwargs['set'], database)

    text = 'You have requested info on the %s timelapse:\n%r\n' \
           'Description: \n%s\n' \
            % (kwargs['set'], timelapse, timelapse.description)
    
    notes = get_notes(timelapse.id, database)
    if notes:
        notes_text = [text, 'Notes:\n']
        logging.info(notes)
        for n in notes:
            notes_text.append(''.join([n.date.strftime('%d %b %Y'), 
                                       '|\t', n.note, '\n']))
        text = ''.join(notes_text)
    edit_message_text(chat_id, message_id, text)

    # set state to start|-1
    to_starting_state(user_id, chat_id, database)


def on_freq_time_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)
    chat_id, message_id = parse_query(query, database)

    if state == 'remind':
        timelapse = get_timelapse_by_id(timelapse_id, database)

        payload = dict(func=kwargs['set'])
        if kwargs['set'] == 'frequency':
            keyboard = create_reply_markup(FREQUENCY_KEYBOARD, **payload)
            text = 'Please specify how often you would like me to ' \
                'remind you about your timelapse *%s*?' % timelapse.title 
        else:
            keyboard = create_reply_markup(HOURS_KEYBOARD, **payload)
            text = 'Please specify the time of day you would like me to ' \
                'remind you about your timelapse *%s*?' % timelapse.title 
 
        edit_message_text(chat_id, message_id, text, reply_markup=keyboard)

        state = kwargs['set'] 
        set_state(user_id, state, timelapse_id, database)

    else:
        if kwargs['func'] == 'frequency':
            for i, v in enumerate(['daily', 'weekly', 'monthly']):
                if v == kwargs['set']:
                    value = i
        else:
            value = datetime.strptime(kwargs['set'], '%H:%M')
        edit_timelapse(timelapse_id, kwargs['func'], value, database)

        timelapse = get_timelapse_by_id(timelapse_id, database)
        text = 'Got it. I will send %s reminder on timelapse *%s*.' \
                % (timelapse.frequency, timelapse.title)
        edit_message_text(chat_id, message_id, text)

        # set state to start|-1
        to_starting_state(user_id, chat_id, database)
 

def on_remind_button(query, database, **kwargs):
    state, timelapse_id, user_id = parse_for_state(query, database)
    chat_id, message_id = parse_query(query, database)

    payload = dict(func='frequency')
    keyboard = create_reply_markup(['time', 'frequency'], **payload)
    text = 'When and how often should I send reminders?'
    edit_message_text(chat_id, message_id, text, reply_markup=keyboard)

    state = 'remind'
    set_state(user_id, state, timelapse_id, database)


CALLBACK_HANDLERS = {
        'edit': on_edit,
        'track': on_track,
        'title': on_title_button,
        'units': on_units_button,
        'duration': on_duration_button,
        'start time': on_start_time_button,
        'description': on_description_button,
        'add note': on_add_note_button,
        'delete': on_delete_button,
        'set reminder': on_remind_button,
        'frequency': on_freq_time_button,
        'time': on_freq_time_button,
        'back': on_main_menu_button,
}


def on_query_update_message(callback_data, query, database):
    try:
        data = loads(callback_data)
    except ValueError:
        return

    handler = data['func']
    logging.info(handler)
    if handler in CALLBACK_HANDLERS:
        CALLBACK_HANDLERS[handler](query, database, **data)


def handle_callback_query(callback_query, database):
    callback_query_id = callback_query.get('id')
    answer_callback_query(callback_query_id)

    callback_data = callback_query.get('data')
    on_query_update_message(callback_data, callback_query, database)


def handle_start(message, database):
    user_info = get_user_info(message)
    chat_id = message.get('chat').get('id')

    first_name = add_user(user_info, database)
    if first_name:
        text = 'Welcome %s! My name is Tim Lapp. I specialize on tracking ' \
               'progress of various kind. Struggling to build a new habit? ' \
               'Create a timelapse to track your success and mark ' \
               'milestones! Type /add *timelapse name* to start something ' \
               'new! I will guide you through the rest of the process.' \
               % first_name
    else:
        text = 'Welcome back %s! To take a look at your timelapses type ' \
                '/track or use /edit command to adjust timelapses to the ' \
                'lastest wishes of your heart. You can always /add *new ' \
                'timelapse* as well!' % user_info['first_name']
        set_state(user_info['id'], 'start', -1, database)
    return send_message(chat_id, text, parse_mode='Markdown')


def handle_add(message, database):
    chat_id = message.get('chat').get('id')
    user_id = message.get('from').get('id')
    timelapse_title = get_timelapse_title(message)

    if timelapse_title:
        timelapse_id = add_timelapse(timelapse_title, user_id, database)
        text = "Yay! Your timelapse '%s' has been created! Perhaps you want " \
               "to tweak it a bit?" % timelapse_title
        keyboard = create_reply_markup(TIMELAPSE_EDIT_KEYBOARD)
        send_message(chat_id, text, reply_markup=keyboard)
    else:
        logging.error('Poor user input. User %d', chat_id)
        text = 'Please provide a name for your brand new timelapse ' \
               '(up to 3 words). Example:\n' \
               '/add MY BEST SUMMER'
        send_message(chat_id, text)

    return timelapse_title


def handle_edit(message, database):
    state, timelapse_id, _  = parse_for_state(message, database)
    chat_id = message.get('chat').get('id')
    user_id = message.get('from').get('id')

    user_timelapses = get_user_timelapses(user_id, database)

    if user_timelapses:
        payload = dict(func='edit')
        keyboard = create_reply_markup(user_timelapses, **payload)

        text = 'Please choose the timelapse you want to edit.'
        send_message(chat_id, text, reply_markup=keyboard)

        state = 'edit'
        set_state(user_id, state, timelapse_id, database)
    
    else:
        text = 'You have none timelapses to edit. Create one by typing /add' \
               ' *new timelapse*.'
        send_message(chat_id, text)
        to_starting_state(user_id, chat_id, database)

    return user_timelapses


def handle_track(message, database):
    state, timelapse_id, _  = parse_for_state(message, database)
    chat_id = message.get('chat').get('id')
    user_id = message.get('from').get('id')

    user_timelapses = get_user_timelapses(user_id, database)
    logging.info(user_timelapses)
    logging.info(type(user_timelapses))
    
    if user_timelapses:
        payload = dict(func='track')
        keyboard = create_reply_markup(user_timelapses, **payload)

        text = 'Please choose the timelapse you want to look at in more ' \
               'details.'
        send_message(chat_id, text, reply_markup=keyboard)

        state = 'track'
        set_state(user_id, state, timelapse_id, database)

    else:
        text = 'You have none timelapses to track. Create one by typing /add' \
               ' *new timelapse*.'
        send_message(chat_id, text)
        to_starting_state(user_id, chat_id, database)

    return user_timelapses


COMMAND_HANDLERS = dict(
    start=handle_start,
    add=handle_add,
    edit=handle_edit,
    track=handle_track,
)


def detect_command(message):
    # TODO parses only one command

    commands = []
    entities = message.get('entities', [])
    text = message.get('text')

    for e in entities:
        if e.get('type') != 'bot_command':
            continue

        for command_name in COMMAND_HANDLERS.keys():
            offset = e.get('offset', 0)
            length = e.get('length', 0)

            if text[offset + 1:offset + 1 + length].startswith(command_name):
                commands.append(command_name)
                break

    logging.info('received commands: %s', commands)
    if commands:
        return commands[0]
    else:
        return 0

def handle_command(command, message, database):
    for command_name, command_handler in COMMAND_HANDLERS.items():
        if command_name == command:
            command_handler(message, database)


def on_start_state(message, database):
    command = detect_command(message)
    if command:
        handle_command(command, message, database)


def on_track_state(message, database):
    pass


MESSAGE_HANDLERS = {
    'title': on_title_button,
    'duration': on_duration_button,
    'start time': on_start_time_button,
    'description': on_description_button,
    'add note': on_add_note_button,
    'start': on_start_state,
    'track': on_track_state,
}


def handle_message(message, database):
    state, timelapse_id, user_id = parse_for_state(message, database)

    if state in MESSAGE_HANDLERS:
        MESSAGE_HANDLERS[state](message, database)

    else:
        chat_id = message.get('chat').get('id')
        to_starting_state(user_id, chat_id, database)


def not_supported(update):
    pass
