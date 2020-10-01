'''
    this file is for storing users data and channels data for iteration 1
    this file only define users and channels data type (list)
    this file will be imported by other files for stroing
    this file will be updated if we need to edit attributions of users and channels
    this file contains standard data for reference (see below)
'''
# last edit 10/01/2020

users = [

]

channels = [
    
]

'''
# here are sample data
# seperate users and channels
users = [
    {
        'u_id': 1,
        'name_first' : 'user1',
        'name_last' : 'last',
        'handle' : 'user1last',
        'email' : 'test@test.com',
        'password' : 'test123',
        'token' : '1', # for iteration 1 
        'channels' : [ ], # a list to store this user's channel(c_id)
    },
    {
        'u_id': 2,
        'name_first' : 'user2',
        'name_last' : 'last',
        'handle' : 'user2last'
        'email' : 'test2@test.com',
        'password' : 'test123',
        'token' : '2', # for iteration 1
        'channels' : [ ], # a list to store this user's channel(c_id)
    },
]

channels = [
    {
        'c_id' : 1,
        'public' : True,
        'name' : 'test channel',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
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
        'c_id' : 2,
        'public' : False,
        'name' : 'test channel2',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
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