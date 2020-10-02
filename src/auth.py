from data import users
from error import InputError
import re


'''
    summary & assumption:
    (check assumption.md for more details)
        1. auth_login and auth_register will not generate a unique token for user.
            token == str(u_id) for iteration 1
        2. auth_logout will always run successfully since we do not have unique token
        
    3 help functions:
        1. is_email_valid(email)
            this function check email validity by oftered method
            return True if valid else return False
        2. email_repeat_check(email)
            this function check duplication of a email
            return corresponding user(dict) if the email refers to an exist user
            else return False
        3. handle generate(name_first, name_last, u_id)
            this function will generate a handle based on name_first and name_last
            if the length of (name_first + name_last) > 20, handle will only contain 
                first 20 characters
            if there exists a same handle in data, new handle will be str(u_id) + handle
            and also cut off at 20 characters
'''

def auth_login(email, password):
    # inputerror when Email entered is not a valid email
    if is_email_valid(email) is False:
        raise InputError()

    # inputerror when Email entered does not belong to a user
    if email_repeat_check(email) is False:
        raise InputError()
    else:
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
    for user in users:
        if user['token'] == token:
            return {
                'is_success' : True
            }
    return {
        'is_success' : False
    }

def auth_register(email, password, name_first, name_last):
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
    new_user = {}
    new_user['u_id'] = len(users) + 1
    new_user['name_first'] = name_first
    new_user['name_last'] = name_last
    new_user['email'] = email
    new_user['password'] = password
    new_user['channels'] = []
    new_user['token'] = str(len(users) + 1)
    new_user['handle'] = handle_generate(name_first, name_last, new_user['u_id'])
    users.append(new_user)
    return {
        'u_id' : new_user['u_id'], 
        'token' : new_user['token'],
    }

### help function

### check email validity by offered method
def is_email_valid(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):  
        return True
    else:
        return False

### check given email is in database or not
### return user(dict) if it exists
###     else return false
def email_repeat_check(email):
    for user in users:
        if user['email'] == email:
            return user
    return False

### generate a handle (first + last) all lowcase
### if it is more than 20 charaters, cutoff at 20
### if it exists in database, combine it with u_id
def handle_generate(name_first, name_last, u_id):
    handle = (name_first + name_last).lower()
    if len(handle) > 20:
        handle = handle[:20]
    for user in users:
        if user['handle'] == handle:
            handle = (str(u_id) + handle)[:20]
    return handle