from data import users, channels
from error import InputError
from helper import is_token_valid, get_uid_from_token
from datetime import datetime
import re

########### GLOBAL VARIABLES ###############
# total number of messages sent at any given time is the message_id of a new message
# messages_sent is reset by clear() in other.py
# global variable used as messages are not persistent (i.e. messages can be removed), 
# which makes it unreliable to use total number of messages at any given time
# as message_id
messages_sent = 1

'''Send a message from authorised_user to the channel specified by channel_id'''
def message_send(token, channel_id, message):
    global messages_sent

    '''InputError when message > 1000 characters'''
    if len(message) > 1000:
        raise InputError
        
    '''AccessError when user hasn't joined the channel'''
    if not is_token_valid(token):
        raise AccessError
    
    '''Send message'''
    new_msg = {}
    new_msg['message_id'] = messages_sent
    new_msg['u_id'] = get_uid_from_token(token)
    new_msg['message'] = message
    new_msg['time_created'] = datetime.now()

    ''' Append message to appropriate channel '''
    channels[channel_id-1]['messages'].append(new_msg)

    messages_sent += 1

    return {
        'message_id': new_msg['message_id']
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
