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

users = [

]

channels = [

]

def create_user(email, password, name_first, name_last, handle):
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
    new_user = {}
    new_user['u_id'] = len(users) + 1
    new_user['name_first'] = name_first
    new_user['name_last'] = name_last
    new_user['email'] = email
    new_user['password'] = password
    new_user['channels'] = []
    new_user['token'] = str(len(users) + 1)
    new_user['handle'] = handle
    users.append(new_user)
    return new_user
