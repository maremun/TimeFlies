#!/usr/bin/env python3
#   encoding: utf8
#   bot.py

import logging

from pprint import pprint
from requests import Session
from .settings import *
from .utils import send_request

def get_updates(offset=None, limit=100, timeout=60, sess=None):
    if not sess:
        sess = Session()
    method = 'getUpdates'
    params = dict(offset=offset, limit=limit, timeout=60)
    json = send_request(method, params, sess)

    if json:
        updates = json.get('result',[])
        method = 'sendMessage'
        said = ' said: '
        for upd in updates:
            m = upd.get('message')
            if m:
                chat_id = m.get('chat').get('id')
                username = m.get('from').get('username')
                message_text = m.get('text')
                text = ''.join([username, said, message_text])
                params = dict(chat_id=chat_id, text=text) 
                json_response = send_request(method, params, sess)
                last_update_id = upd.get('update_id')
        
        return json_response, last_update_id
    return 'request failed, see logging for details.'

def main():
    sess = Session()
    offset = 0

    while True:
        updates, offset = get_updates(offset=offset, sess=sess)
        offset += 1
        pprint(updates)


if __name__ == '__main__':
    main()
