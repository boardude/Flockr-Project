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
import random
import string
from data import users, channels
from auth import auth_register, auth_login
from error import AccessError

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

def get_random_str(length):
    """
        Generates random string with the combination of lower-
        and upper-case letters
    """
    letters = string.ascii_letters
    random_str = ''.join(random.choice(letters) for i in range(length))

    return random_str
