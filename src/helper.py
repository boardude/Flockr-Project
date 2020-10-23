import random
import string
from data import users, channels
from auth import auth_register, auth_login

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

def get_user_from_token_naive(token): # temporary function
    '''
    no decode
    '''
    for user in users:
        if user['token'] == token:
            return user

def get_user_from_id(u_id):
    '''
        Returns a user with given u_id if it exists in data,
        else return None
    '''
    try:
        return users[u_id-1]
    except IndexError:
        return None

def get_channel_from_id(channel_id):
    '''
        Return a channel with given channel_id if it exists in data,
        else return None
    '''
    try:
        return channels[channel_id-1]
    except IndexError:
        return None

