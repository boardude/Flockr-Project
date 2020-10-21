'''
import data.py for data storing
import error.py for error raising
import re module for checking email address
'''

import re
from data import users, create_user
from error import InputError, AccessError


def auth_login(email, password):
    '''
    This will activate a user with given email address and password.
    It will generate a valid token for the user to remain authenticated.
    It will return a dictionary with right data if success, else raise errors.

    Args:
        param1: user's email.
        param2: password.

    Returns:
        This will return a dictionary.
        {
            'u_id' :
            'token' :
        }

    Raises:
        InputError: 1. Email entered is not a valid email.
                    2. Email entered does not belong to a user.
                    3. Password is not correct
    '''
    if is_email_valid(email) is False:
        raise InputError()

    # inputerror when Email entered does not belong to a user
    if email_repeat_check(email) is False:
        raise InputError()
    user = email_repeat_check(email)

    # inputerror when Password is not correct
    if user['password'] != password:
        raise InputError()

    # to do
    # auth_login will not generate a unique token for user
    # we will finish it in iteration 2
    return {
        'u_id' : user['u_id'],
        'token' : user['token']
    }

def auth_logout(token):
    '''
    This will invalidate user with given token to log the user out.
    This will return a dictionary with success information if success,
    else raise errors.

    Args:
        param1: token

    Returns:
        This will return a dictionary.
        {
            'is_success' : (boolean)
        }

    Raises:
        AccessError: token does not refer to a valid token
    '''
    for user in users:
        if user['token'] == token:
            return {
                'is_success' : True
            }
    raise AccessError()

def auth_register(email, password, name_first, name_last):
    '''
    This will create a new user in data with given information.
    This will also create a handle for user relative to user's name.
    This will return a new token for authentication in their session.

    Args:
        param1: email
        param2: password
        param3: first name
        param4: last name

    Returns:
        This will return a dictionary.
        {
            'u_id' :
            'token' :
        }

    Raises:
        InputError: 1. Email entered is not a valid email.
                    2. Email address is already being used by another user.
                    3. Password entered is less than 6 characters long.
                    4. name_first not is between 1 and 50 characters inclusively in length.
                    5. name_last is not between 1 and 50 characters inclusively in length.
    '''
    # inputerror when Email entered is not a valid email
    if is_email_valid(email) is False:
        raise InputError()

    # inputerror when Email address is already being used by another user
    if email_repeat_check(email) is not False:
        raise InputError()

    # password length check
    if len(password) < 6:
        raise InputError()
    if len(name_first) == 0 or len(name_last) == 0:
        raise InputError()
    if len(name_first) > 50 or len(name_last) > 50:
        raise InputError()

    # check data.py for more details of data storing
    handle = handle_generate(name_first, name_last, len(users) + 1)
    new_user = create_user(email, password, name_first, name_last, handle)
    return {
        'u_id' : new_user['u_id'],
        'token' : new_user['token'],
    }

### 3 helper functions
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

def email_repeat_check(email):
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
    return False


def handle_generate(name_first, name_last, u_id):
    '''
    This is a simple helper function to generate a handle(string) which combines
    user's first name and last name(all low case).
    If length of handle is more than 20, it will cut it at 20th characters.
    If generated handle is duplicate in data, it will add user's u_id to handle
    like this handle = str(u_id) + origin_handle.

    Args:
        param1: first name
        param2: last name
        param3: u_id

    Returns:
        This will return a handle (string) which contains first name and last name.

    Raises:
        This will not raise any error.
    '''
    handle = (name_first + name_last).lower()
    if len(handle) > 20:
        handle = handle[:20]
    for user in users:
        if user['handle'] == handle:
            handle = (str(u_id) + handle)[:20]
    return handle
