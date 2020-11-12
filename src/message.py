'''
import users and channels from data to manipulate data
import error for error raising
import datatime for creating timestamp
'''
import threading
import time
from data import create_new_msg
from helper import get_channel_from_id, get_user_from_token, is_user_an_owner
from error import InputError, AccessError

def message_send(token, channel_id, message):
    '''
    This function will send a message from authorised_user
    to the channel specified by channel_id.
    It will create a unique msg_id for new message.
    msg_id = channel_id * 10000 + the order in that channel.
    For example, the third message in channel 6 would have a
    msg_id with 600003.

    Args:
        param1: authorised user's token
        param2: id of target channel
        param3: new message

    Returns:
        it will return a dictionary of new message id.

    Raises:
        InputError:
            Message is more than 1000 characters
        AccessError:
            1. given token does not refer to a valid user
            2. the authorised user has not joined the channel with channel_id
    '''
    auth_user = get_user_from_token(token)
    channel = get_channel_from_id(channel_id)
    # AccessError when given token does not refer to a valid user
    if auth_user is None:
        raise AccessError(description='Invalid token.')
    #InputError when message > 1000 characters
    if len(message) > 1000:
        raise InputError(description='Message exceeds 1000 characters.')
    #AccessError when user hasn't joined the channel
    if channel is None:
        raise AccessError(description='Invalid channel.')
    if auth_user['u_id'] not in channel['all_members']:
        raise AccessError(description='User is not a member of channel.')

    #Send message
    new_msg = create_new_msg(message, channel, auth_user['u_id'])
    channel['latest_msg_id'] += 1
    channel['messages'].append(new_msg)
    return {
        'message_id': new_msg['message_id']
    }

def message_remove(token, message_id):
    '''
    This function will remove the message with given message_id.

    Args:
        param1: authorised user's token
        param2: target message_id

    Returns:
        it will return an empty dictionary

    Raises:
        InputError:
            Message (based on ID) no longer exists
        AccessError:
            1. given token does not refer to a valid user
            2. Message with message_id was sent by the authorised user making this request
            3. The authorised user is an owner of this channel or the flockr
    '''
    auth_user = get_user_from_token(token)
    msg_info = get_message_info(message_id)

    # access error when given token does not refer to a valid user
    if auth_user is None:
        raise AccessError(description='Invalid token.')

    # input error when given message_id does not refer to a valid message
    if msg_info is None:
        raise InputError(description='Invalid message ID.')

    # access error when auth user does not have permission
    permittd = False
    if msg_info['u_id'] == auth_user['u_id']:
        permittd = True
    if is_user_an_owner(token, msg_info['channel_id']) is True:
        permittd = True
    if permittd is False:
        raise AccessError(description='User must be an owner.')

    # do remove work
    msg_info['msg_list'].remove(msg_info['message'])
    return {
    }

def message_edit(token, message_id, message):
    '''
    This function will edit the message with given message_id.
    if given message is empty, it will detele that message

    Args:
        param1: authorised user's token
        param2: target message_id
        param3: new message

    Returns:
        it will return an empty dictionary

    Raises:
        AccessError:
            1. given token does not refer to a valid user
            2. Message with message_id was sent by the authorised user making this request
            3. The authorised user is an owner of this channel or the flockr
    '''
    # check entered message, if it's empty, call remove func
    if message == '':
        message_remove(token, message_id)
        return {
        }

    auth_user = get_user_from_token(token)
    msg_info = get_message_info(message_id)
    # access error when given token does not refer to a valid user
    if auth_user is None:
        raise AccessError(description='Invalid token')

    # access error when auth user does not have permission
    permittd = False
    if msg_info['u_id'] == auth_user['u_id']:
        permittd = True
    if is_user_an_owner(token, msg_info['channel_id']) is True:
        permittd = True
    if permittd is False:
        raise AccessError(description='User must be an owner')

    # do edit work
    for msg in msg_info['msg_list']:
        if msg['message_id'] == message_id:
            msg['message'] = message
    return {
    }

def get_message_info(message_id):
    '''
    This is a helper function.
    It will return a message with given message_id

    Args:
        param1: target message_id

    Returns:
        it will return message_info with given message_id if it exists,
        else return None to represent no such a message.
        {
            'message' : msg,
            'u_id' : msg['u_id'],
            'channel_id' : channel_id,
            'msg_list' : channel['messages'],
        }
    '''
    channel_id = int(str(message_id)[:-4])
    channel = get_channel_from_id(channel_id)
    if channel is None:
        return None
    for msg in channel['messages']:
        if msg['message_id'] == message_id:
            return {
                'message' : msg,
                'u_id' : msg['u_id'],
                'channel_id' : channel_id,
                'msg_list' : channel['messages'],
                'reactors' : msg['reactors'],
                'pinned' : msg['pinned']
            }
    return None

def message_send_later(token, channel_id, message, time_sent):
    '''
    This function will send a message from an authorised user to the channel
    specified by channel_id automatically at a specified time in the future.

    Args:
        param1(str): authorised uesr's token
        param2(int): id of target channel
        param3(str): sent message
        param4(int): unix_timestamp, a future time

    Returns:
        It will return a dict with message_id

    Raises:
        InputError if:
            - Channel_id is invalid
            - Message is more than 1000 characters
            - Time sent is a time in the past

        AccessError if:
            - when the authorised use hasn't joined the channel
            - when given token is invalid
    '''
    ## Errors
    auth_user = get_user_from_token(token)
    channel = get_channel_from_id(channel_id)
    # access error when given token does not refer to a valid user
    if auth_user is None:
        raise AccessError(description='Invalid token')
    # input error when given channel_id is invalid
    if channel is None:
        raise InputError(description='Invalid channel.')
    # access error when the authorised use hasn't joined the channel
    if auth_user['u_id'] not in channel['all_members']:
        raise AccessError(description='User is not a member of channel.')
    # input error when message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='Message exceeds 1000 characters.')

    ### InputError for time in past
    countdown = time_sent - int(time.time())
    if countdown < 0:
        raise InputError(description='past time given')

    ### Initiate timer for message_send function
    new_msg = create_new_msg(message, channel, auth_user['u_id'])
    channel['latest_msg_id'] += 1
    timer = threading.Timer(countdown, append_msg_to_channel, args=[new_msg, channel])
    timer.start()
    return {
        'message_id': new_msg['message_id']
    }

def message_react(token, message_id, react_id):
    '''given a message with a channel the authorised user is a part of, adds
    a 'react' to that message'''
    
    auth_user = get_user_from_token(token)
    channel = get_channel_from_id(get_message_info(message_id)['channel_id'])
    message = get_message_info(message_id)
    ### InputError: User is not part of channel with the message
    if auth_user['u_id'] not in channel['all_members']:
        raise InputError(description='User is not a member of channel.')
    
    ### InputError: React ID invalid (not 1)
    if react_id != 1:
        raise InputError(description='Invalid react_id')
    
    ### InputError: React ID already contained by user
    if auth_user['u_id'] in message['reactors']:
        raise InputError(description='user has already reacted')
        
    ### react to message
    message['reactors'].append(auth_user['u_id'])
    
    return {
    }
    
def message_unreact(token, message_id, react_id):
    '''given a message with a channel the authorised user is a part of, removes
    a 'react' to that message'''
    
    auth_user = get_user_from_token(token)
    channel = get_channel_from_id(get_message_info(message_id)['channel_id'])
    message = get_message_info(message_id)
    ### InputError: User is not part of channel with the message
    if auth_user['u_id'] not in channel['all_members']:
        raise InputError(description='User is not a member of channel.')
    
    ### InputError: React ID invalid (not 1)
    if react_id != 1:
        raise InputError(description='Invalid react_id')
    
    ### InputError: React ID already not containd by user
    if auth_user['u_id'] not in message['reactors']:
        raise InputError(description='user hasnt reacted')
        
    ### unreact to message
    message['reactors'].remove(auth_user['u_id'])
    
    return {
    }

def message_pin(token, message_id):
    '''
    This function marks a message as 'pinned' to be given special viewership 
    on the frontend
    '''
    auth_user = get_user_from_token(token)
    channel = get_channel_from_id(get_message_info(message_id)['channel_id'])
    ### InputError if message_id is invalid
    if get_message_info(message_id) == None:
        raise InputError(description='Not a valid message')
    
    message = get_message_info(message_id)
    ### InputError if message_id is already pinned
    if message['pinned'] == True:
        raise InputError (description='Message already pinned')
    
    ### AccessError if user is not a member of the channel
    if auth_user['u_id'] not in channel['all_members']:
        raise AccessError(description='User isnt a member of the channel')
    
    ### AccessError if user is not an owner of the channel
    if auth_user['u_id'] not in channel['owner_members']:
        raise AccessError(description='User isnt an owner of the channel')
    
    ### Pin message
    message['pinned'] = True

def message_unpin(token, message_id):
    
    auth_user = get_user_from_token(token)
    channel = get_channel_from_id(get_message_info(message_id)['channel_id'])
    ### InputError if message_id is invalid
    if get_message_info(message_id) == None:
        raise InputError(description='Not a valid message')
    
    message = get_message_info(message_id)
    ### InputError if message_id is already unpinned
    if message['pinned'] == False:
        raise InputError (description='Message already pinned')
    
    ### AccessError if user is not a member of the channel
    if auth_user['u_id'] not in channel['all_members']:
        raise AccessError(description='User isnt a member of the channel')
    
    ### AccessError if user is not an owner of the channel
    if auth_user['u_id'] not in channel['owner_members']:
        raise AccessError(description='User isnt an owner of the channel')
    
    ### Pin message
    message['pinned'] = False
    
def append_msg_to_channel(new_msg, channel):
    '''
    This is a simple helper function to append msg to channel

    Args:
        param1(dict): message to append
        param2(dict): target channel
    '''
    channel['messages'].append(new_msg)
