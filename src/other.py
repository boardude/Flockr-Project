# Yicheng (Mike) Zhu
# Last updated 20/10/2020

"""
    data module contains users and channels list structures to store associated
    data

    auth module allows us to use auth_register() and auth_login() to register
    and log in test users
"""

from data import users, channels
from auth import auth_register, auth_login

def clear():
    """
        Resets flockr data by removing all elements of "users" and "channels"
        lists in data module
    """

    while len(users) != 0:
        del users[0]
    while len(channels) != 0:
        del channels[0]
    pass

def users_all(token):
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        ],
    }

def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

############ UNIVERSAL HELPER FUNCTIONS #########
def register_and_login(email, password, first_name, last_name):
    """
        Registers and logs in user with provided details,
        returning the token

    """
    auth_register(email, password, first_name, last_name)
    login = auth_login(email, password)
    return login['token']

def is_token_valid(token):
    """
        Returns True if token is valid (token is found in users list), otherwise False
    """
    for user in users:
        if user['token'] is token:
            return True
    return False

def get_uid_from_token(token):
    """
        Return the corresponding u_id when given the token of an authorised
        user
    """
    for user in users:
        if user['token'] == token:
            return user['u_id']

    return None
