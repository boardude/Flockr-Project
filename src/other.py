# Yicheng (Mike) Zhu
# Last updated 22/10/2020

"""
    random and string modules allow for random string generation
    for invalid token tests

    data module contains users and channels list structures to store associated
    data

    auth module allows us to use auth_register() and auth_login() to register
    and log in test users
"""

from data import users, channels
from error import InputError, AccessError
from helper import get_user_from_token, get_user_from_id, get_channel_from_id

def clear():
    """
        Resets flockr data by removing all elements of "users" and "channels"
        lists in data module
    """
    users.clear()
    channels.clear()
    return {
    }

def users_all(token):
    # check token validity
    if get_user_from_token(token) is None:
        raise AccessError()

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
    # check u_id validity
    user = get_user_from_id(u_id)
    if user is None:
        raise InputError

    # check permission_id validity
    if permission_id not in [1, 2]:
        raise InputError

    # check token validity
    if get_user_from_token(token) is None:
        raise AccessError

    # check if token refers to an owner
    admin = get_user_from_token(token)
    if admin['permission_id'] != 1:
        raise AccessError

    # change permission of u_id user to permission_id
    user['permission_id'] = permission_id

    return {
    }

def search(token, query_str):
    # check token validity
    if get_user_from_token(token) is None:
        raise AccessError

    result = []
    user = get_user_from_token(token)

    # search for messages with query string
    for channel_id in user['channels']:
        channel = get_channel_from_id(channel_id)
        for message in channel['messages']:
            if query_str in message['message']:
                result.append(message)
    
    return {
        'messages': result
    }
