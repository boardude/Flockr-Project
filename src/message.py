'''
import users and channels from data to manipulate data
import error for error raising
import datatime for creating timestamp
'''
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
        raise AccessError()
    #InputError when message > 1000 characters
    if len(message) > 1000:
        raise InputError()
    #AccessError when user hasn't joined the channel
    if auth_user['u_id'] not in channel['all_members']:
        raise AccessError()

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
        raise AccessError()

    # input error when given message_id does not refer to a valid message
    if msg_info is None:
        raise InputError()

    # accee error when auth user does not have permission
    permittd = False
    if msg_info['u_id'] == auth_user['u_id']:
        permittd = True
    if is_user_an_owner(token, msg_info['channel_id']) is True:
        permittd = True
    if permittd is False:
        raise AccessError()

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
        raise AccessError()

    # access error when auth user does not have permission
    permittd = False
    if msg_info['u_id'] == auth_user['u_id']:
        permittd = True
    if is_user_an_owner(token, msg_info['channel_id']) is True:
        permittd = True
    if permittd is False:
        raise AccessError()

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
            }
    return None
