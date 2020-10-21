# Yicheng (Mike) Zhu
# Last updated 20/10/2020

"""
    random and string modules allow for random string generation
    for invalid token tests

    data module contains users and channels list structures to store associated
    data

    auth module allows us to use auth_register() and auth_login() to register
    and log in test users
"""

from data import users, channels
from error import AccessError
from message import messages_sent
from helper import is_token_valid, get_uid_from_token

def clear():
    """
        Resets flockr data by removing all elements of "users" and "channels"
        lists in data module
    """

    while len(users) != 0:
        del users[0]
    while len(channels) != 0:
        del channels[0]
    
    messages_sent = 1

def users_all(token):
    # check token validity
    if not is_token_valid(token):
        raise AccessError

    all_users = []
    for user in users:
        user_details = {}
        user_details['u_id'] = user['u_id']
        user_details['email'] = user['email']
        user_details['name_first'] = user['name_first']
        user_details['name_last'] = user['name_last']
        user_details['handle_str'] = user['handle']
        all_users.append(user_details)
    
    return {
        'users': all_users,
    }

def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    # check token validity
    if not is_token_valid(token):
        raise AccessError

    result = []
    u_id = get_uid_from_token(token)

    # search for messages with query string
    for channel in channels:
        for message in channel['messages']:
            if message['u_id'] == u_id:
                if query_str in message['message']:
                    result.append(message)
    
    return {
        'messages': result
    }

    return random_str
