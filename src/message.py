'''functions for flock messaging, including sending, removing, and editing messages'''

from data import users, channels
from error import InputError, AccessError
from datetime import datetime

def message_send(token, channel_id, message):
    '''Send a message from authorised_user to the channel specified
    by channel_id'''
    #InputError when message > 1000 characters
    if len(message) > 1000:
        raise InputError

    #AccessError when user hasn't joined the channel
    for token_ in users:
        if token_.get('u_id') == token:
            if token_.get('channels').index(channel_id) == ValueError:
                raise AccessError

    #Send message
    new_msg = {}
    new_msg_id = 0
    new_msg['u_id'] = token
    new_msg['time_created'] = datetime.today()
    new_msg['message'] = message
    for chan in channels:
        if chan.get('channel_id') == channel_id:
            new_msg_id = (1000 * channel_id) + len(chan.get('messages'))
            new_msg['message_id'] = new_msg_id
            chan.get('messages').append(new_msg)
    return {
        'message_id': new_msg_id
    }


def message_remove(token, message_id):
    '''Given a message_id for a message, this message is removed from the channel'''

    is_message = False
    is_from_user = True

    #AccessError if user not an owner
    for user in users:
        if user.get('token') == token:
            for chan in user.get('channels'):
                if chan != message_id - 1000:
                    raise AccessError

    #Remove message
    for chan in channels:
        for msg in chan.get('messages'):
            if msg.get('message_id') == message_id:
                is_message = True
                if msg.get('u_id') == token:
                    msg.pop()
                else:
                    is_from_user = False

    #InputError if message from message_id doesn't exist
    if not is_message:
        raise InputError

    #AccessError if message not sent from auth user
    if not is_from_user:
        raise AccessError

    return {
    }

def message_edit(token, message_id, message):
    '''Given a message, update it's text with new text. If the new
    message is an empty string, the message is deleted'''

    #AccessError if user not an owner
    for user in users:
        if user.get('token') == token:
            for chan in user.get('channels'):
                if chan != message_id - 1000:
                    raise AccessError

    #InputError when message > 1000 characters
    if len(message) > 1000:
        raise InputError

    #edit message
    for chan in channels:
        for msg in chan.get('messages'):
            if msg.get('message_id') == message_id:
                if msg.get('u_id') != token:
                    raise AccessError
                if message == '':
                    message_remove(token, message_id)
                else:
                    msg['message'] = message

    return {
    }
