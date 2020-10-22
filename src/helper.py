import random
import string
from data import users, channels
from auth import auth_register, auth_login
import re
import jwt
SECRET = 'grape6'

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

def is_email_valid(email):
    '''
    This is a simple helper function to test email validity.
    This will return True if email is valid, else return False

    Args:
        param1: email

    Returns:
        This will return a boolean value.
        True for valid, False for invalid.

    Raises:
        This will not raise any error.
    '''
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    return False

def get_user_from_email(email):
    '''
    This is a simple helper function to test email duplication.
    This will return corresponding user data if email is duplicate, else return False

    Args:
        param1: email

    Returns:
        This will return user(a dictionary) if the email is relative to a
        certain user, else return False.

    Raises:
        This will not raise any error.
    '''
    for user in users:
        if user['email'] == email:
            return user
    return None

def get_user_from_id(u_id):
    '''
    This is a simple helper function.
    It will return a user with given u_id if it exists in data,
    else return False

    Args:
        param1: u_id

    Returns:
        This will return uesr(dictionary) if u_id refers to a valid user in data,
        else return False.

    Raises:
        this will not raise any error
    '''
    for user in users:
        if user['u_id'] == u_id:
            return user
    return None

def get_user_from_token(token):
    '''
    invalid token
    1. we cannot decode
    2. logout 
    '''
    try:
        info = jwt.decode(token.encode('utf-8'), SECRET, algorithms=['HS256'])
        if info['has_login'] is False:
            return None
        for user in users:
            if user['u_id'] == info['u_id']:
                return user
    except:
        return None

def get_user_from_token_naive(token): # temporary function
    '''
    no decode
    '''
    for user in users:
        if user['token'] == token:
            return user

def get_channel_from_id(channel_id):
    '''
    This is a simple helper function.
    It will return a channel with given channel_id if it exists in data,
    else return False

    Args:
        param1: channel_id

    Returns:
        This will return channel(dictionary) if token refers to a valid chanenl in data,
        else return False.

    Raises:
        this will not raise any error
    '''
    for channel in channels:
        if channel['channel_id'] == channel_id:
            return channel
    return None


def is_user_in_channel(token, channel_id):
    '''
    This is a simple helper function.
    It will test whether a user with given token is in target channel.

    Args:
        param1: token

    Returns:
        This will return a boolean value.
        It will return True if the user is in target channel.
        else return False.

    Raises:
        this will not raise any error
    '''
    user = get_user_from_token(token)
    if user is None:
        return False
    for channel in user['channels']:
        if channel == channel_id:
            return True
    return False

def is_user_an_owner(token, channel_id):
    user = get_user_from_token(token)
    channel = get_channel_from_id(channel_id)
    if user['u_id'] == 1:
        return True
    if user['u_id'] in channel['owner_members']:
        return True
    return False