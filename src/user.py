'''
import users to access data
import AccessError and InputError for error raising
import re module for email checking
'''
from error import AccessError, InputError
from data import users
from helper import get_user_from_token, get_user_from_id
from auth import is_email_valid

def user_profile(token, u_id):
    '''
    This function is for showing user's profile.
    It will return the information of user's file.

    Args:
        param1: authorised user's token
        param2: authorised user's u_id

    Returns:
        a dictionary containing profile
        {
            'user': {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        }

    Raises:
        InputError: User with u_id is not a valid user
        AccessError: given token does not refer to a valid user
    '''
    request_user = get_user_from_token(token)
    target_user = get_user_from_id(u_id)
    # raise AccessError when given token does not refer to a valid user
    if request_user is None:
        raise AccessError(description='Token does not refer to a valid user')

    # raise InputError when given u_id is not correct
    if target_user is None:
        raise InputError(description='u_id is not correct')

    return {
        'user' : {
            'u_id' : target_user['u_id'],
            'email' : target_user['email'],
            'name_first' : target_user['name_first'],
            'name_last' : target_user['name_last'],
            'handle_str' : target_user['handle'],
        },
    }

def user_profile_setname(token, name_first, name_last):
    '''
    This function is for updating the authorised user's first and last name.

    Args:
        param1: authorised user's token
        param2: new first name
        param3: new last name

    Returns:
        it will return an empty dictionary

    Raises:
        InputError:
            1. name_first is not between 1 and 50 characters inclusively in length
            2. name_last is not between 1 and 50 characters inclusively in length
        AccessError: given token does not refer to a valid user
    '''
    request_user = get_user_from_token(token)
    # raise AccessError when given token does not refer to a valid user
    if request_user is None:
        raise AccessError(description='token does not refer to a valid user')

    if len(name_first) == 0 or len(name_last) == 0:
        raise InputError(description='length of name_first is zero')
    if len(name_first) > 50 or len(name_last) > 50:
        raise InputError(description='length of name_first is greater than 50')

    request_user['name_first'] = name_first
    request_user['name_last'] = name_last
    return {
    }

def user_profile_setemail(token, email):
    '''
    This function is for updating the authorised user's email.

    Args:
        param1: authorised user's token
        param2: new email

    Returns:
        it will return an empty dictionary

    Raises:
        InputError:
            1. Email entered is not a valid email
            2. Email address is already being used by another user
        AccessError: given token does not refer to a valid user
    '''
    request_user = get_user_from_token(token)
    # raise AccessError when given token does not refer to a valid user
    if request_user is None:
        raise AccessError(description='Token does not refer to a valid user')

    # raise InputError when new email is invalid
    if is_email_valid(email) is False:
        raise InputError(description='New email is invalid')

    # raise InputError when new email has been occupied
    for user in users:
        if user['email'] == email:
            raise InputError(description='New email has been occupied')

    request_user['email'] = email
    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    This function is for updating the authorised user's handle.

    Args:
        param1: authorised user's token
        param2: new handle

    Returns:
        it will return an empty dictionary

    Raises:
        InputError:
            1. handle_str in not between 3 and 20 characters inclusive
            2. handle is already used by another user
        AccessError: given token does not refer to a valid user
    '''
    request_user = get_user_from_token(token)
    # raise AccessError when given token does not refer to a valid user
    if request_user is None:
        raise AccessError(description='token does not refer to a valid user')

    # raise InputError if the length of handle is not valid
    if len(handle_str) > 20 or len(handle_str) < 3:
        raise InputError(description='length of handle is not valid')

    # raise InputError if new handle has been occupied by someone
    for user in users:
        if user['handle'] == handle_str:
            raise InputError(description='new handle has been occupied by someone')

    request_user['handle'] = handle_str
    return {
    }
