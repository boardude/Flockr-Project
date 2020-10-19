import data
from error import InputError
import re

'''Send a message from authorised_user to the channel specified by channel_id'''
def message_send(token, channel_id, message):
    
    '''InputError when message > 1000 characters'''
    if len(message) > 1000:
        raise InputError
        
    '''AccessError when user hasn't joined the channel'''
    for token_ in users:
        if token_.get('u_id') == token:
            if token_.get('channels').index(channel_id):
                break
            else:
                raise AccessError
    
    '''Send message'''
    new_msg = {}
    new_msg_id = 0
    new_msg['u_id'] = token
    new_msg['message'] = message
    for chan in channels:
        if chan.get('channel_id') == channel_id:
            new_msg_id = (1000 * channel_id) + len(chan.get('messages'))
            new_msg['message_id'] = new_msg_id
            chan.get('messages').append(new_msg)
    return {
        'message_id': new_msg_id
    }
    
    
'''Given a message_id for a message, this message is removed from the channel'''
def message_remove(token, message_id):

    is_message = False
    is_from_user = True
    
    '''AccessError if user not an owner'''
    for user in users:
        if user.get('token') == token:
            for chan in user.get('channels'):
                if chan != message_id - 1000:
                    raise AccessError

    '''Remove message'''
    for chan in channels:
        for msg in chan.get('messages'):
            if msg.get('message_id') == message_id:
                is_message = True
                if msg.get('u_id'):
                    pop(msg)
                else:
                    is_from_user = False         
    
    '''InputError if message from message_id doesn't exist'''
    if is_message == False:
        raise InputError
    
    '''AccessError if message not sent from auth user'''
    if is_from_user == False:
        raise AccessError

    return {
    }

'''Given a message, update it's text with new text. If the new message is an empty string, the message is deleted'''
def message_edit(token, message_id, message):
    
    is_from_user = False
    is_owner = False
    
    '''AccessError if user not an owner'''
    for user in users:
        if user.get('token') == token:
            for chan in user.get('channels'):
                if chan != message_id - 1000:
                    raise AccessError
    
    '''InputError when message > 1000 characters'''
    if len(message) > 1000:
        raise InputError
        
    for chan in channels:
        for msg in chan.get('messages'):
            if msg.get('message_id') == message_id:
                if msg.get('u_id') != token:
                    raise AccessError
                elif message == '':
                    pop(msg)
                else: 
                    msg['message'] = message
    
    return {
    }
