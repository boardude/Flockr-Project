from data import users
from error import InputError
import re

def auth_login(email, password):
    if is_email_valid(email) is False:
        raise InputError()

    if email_repeat_check(email) is False:
        raise InputError()
    else:
        user = email_repeat_check(email)

    if user['password'] != password:
        raise InputError()
    
    return {
        'u_id' : user['u_id'],
        'token' : user['token']
    }

### need further codes in iteration 2
### assumption!!!!
### always log out successfully in iteration 1
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
    if is_email_valid(email) is False:
        raise InputError()
    if email_repeat_check(email) is not False:
        raise InputError()
    if len(password) < 6:
        raise InputError()
    if len(name_first) == 0 or len(name_last) == 0:
        raise InputError()
    if len(name_first) > 50 or len(name_last) > 50:
        raise InputError()
    new_user = {}
    new_user['u_id'] = len(users) + 1
    new_user['name_first'] = name_first
    new_user['name_last'] = name_last
    new_user['email'] = email
    new_user['password'] = password
    new_user['channel'] = []
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