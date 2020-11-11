'''
    this file is for storing users data and channels data for iteration 1
    this file only define users and channels data type (list)
    this file will be imported by other files for stroing
    this file will be updated if we need to edit attributions of users and channels
    this file contains standard data for reference (see below)
#here are sample data
#seperate users and channels
users = [
    {
        'u_id': 1,
        'name_first' : 'user1',
        'name_last' : 'last',
        'handle' : 'user1last',
        'email' : 'test@test.com',
        'password' : 'test123',
        'reset_code' : '',
        'token' : '1', # for iteration 1
        'channels' : [ ], # a list to store this user's channel(channel_id)
    },
    {
        'u_id': 2,
        'name_first' : 'user2',
        'name_last' : 'last',
        'handle' : 'user2last'
        'email' : 'test2@test.com',
        'password' : 'test123',
        'reset_code' : '',
        'token' : '2', # for iteration 1
        'channels' : [ ], # a list to store this user's channel(channel_id)
    },
]

channels = [
    {
        'channel_id' : 1,
        'public' : True,
        'name' : 'test channel',
        'owner_members': [1, 2], # a list of u_id
        'all_members': [1, 2], # a list of u_id
        'messages' : [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            },
        ],
        'latest_msg_id' : an int start from 0
    },
    {
        'channel_id' : 2,
        'public' : False,
        'name' : 'test channel2',
        'owner_members': [1, 2], # a list of u_id
        'all_members': [1, 2], # a list of u_id
        'messages' : [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            },
        ],
        'latest_msg_id' : an int start from 0
    },
]
'''
# 2nd edition 10/01/2020 daoting
#   add commends and a sample

# 3rd edition 10/02/2020 daoting
#   redefine owner_members and all_members of channels
#   a list of dict --> a list of int(u_id)

# 4th edition 10/14/2020 daoting
#   create a function called create_user for creating user
#   delete relevant part in auth.py

# 5th edition 19/10/2020 Yicheng (Mike) Zhu
#   Created a function called create_new_channel for creating
#   a new channel to replace a code block previously in
#   channels.py.

# 6th edition 10/22/2020 daoting
#   create a new function called create_new_msg
#   add a attribute called latest_msg_id to each channel

# 7th edition 11/08/2020 daoting
#   add new attribute (reset_code) to user
#   the default value should be an empty str
#   after program calls reset_req, an unique code would be stored in reset_code

import time

users = [

]

channels = [

]

def create_user(email, password, name_first, name_last, handle, token):
    '''
    This is a simple helper function to create a new user with given information.
    This will append new user to the list of users.

    Args:
        param1: email
        param2: password
        param3: first name
        param4: last name
        param5: handle

    Returns:
        This will return a dictionary which contains user's information.

    Raises:
        This will not raise any error.
    '''
    new_user = {
        'u_id' : len(users) + 1,
        'name_first' : name_first,
        'name_last' : name_last,
        'email' : email,
        'password' : password,
        'channels' : [],
        'token' : token,
        'handle' : handle,
        'reset_code' : '',
    }
    if new_user['u_id'] == 1:
        new_user['permission_id'] = 1
    else:
        new_user['permission_id'] = 2
    users.append(new_user)
    return new_user

def create_new_channel(channel_id, is_public, name, uid):
    '''
    This is a simple helper function to create a new channel with given its
    channel_id, is_public attribute, name, and the user id of the creator of
    the channel. It will also append the new channel to the channels list in
    this module.

    Returns:
        This will return a dictionary which contains the new channel's details.

    Raises:
        This will not raise any error.
    '''

    new_channel = {}
    new_channel['channel_id'] = channel_id
    new_channel['public'] = is_public
    new_channel['name'] = name
    new_channel['owner_members'] = [uid]
    new_channel['all_members'] = [uid]
    new_channel['messages'] = []
    new_channel['latest_msg_id'] = 0

    # add new channel to channels list
    channels.append(new_channel)

    return new_channel

def create_new_msg(message, channel, u_id):
    '''
    This is an helper function to create a new message.
    It will create a timestamp to represent create time.
    It will create a unique msg_id combining channel_id and channel's msgs

    Args:
        param1: message body (str)
        param2: target channel
        param3: creater's u_id

    Returns:
        it will return a dictionary of new_msg
        {
            'message_id' : msg_id,
            'u_id' : u_id,
            'message' : message,
            'time_created': timestamp,
        }
    '''
    timestamp = int(time.time())
    msg_id = channel['channel_id'] * 10000 + channel['latest_msg_id'] + 1
    new_msg = {
        'message_id' : msg_id,
        'u_id' : u_id,
        'message' : message,
        'time_created': timestamp,
        'reactors': []
    }
    return new_msg
