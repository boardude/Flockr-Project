# Yicheng (Mike) Zhu
# Last updated 21/10/2020

"""
    pytest module allows us to test if exceptions are thrown at appropriate times

    other module contains user_all function that we need to test, as well as useful
    helper functions

    data module contains data on users stored in a "users" list

    error module defines an AccessError exception that is to be thrown when
    an invalid token is passed
"""

import pytest
from other import users_all, clear
from auth import auth_login, auth_register
from user import user_profile_sethandle
from data import users
from error import AccessError

@pytest.fixture
def create_users():
    clear()
    auth_register('validuseremail@gmail.com', 'validpass', 'User', 'One')
    auth_register('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    auth_register('validuser3email@gmail.com', 'validpass3', 'User', 'Three')
    auth_login('validuseremail@gmail.com', 'validpass')
    auth_login('validuser2email@gmail.com', 'validpass2')
    auth_login('validuser3email@gmail.com', 'validpass3')

def test_all_invalid_token(create_users):
    # empty
    with pytest.raises(AccessError):
        users_all('')

    # None
    with pytest.raises(AccessError):
        users_all(None)

    # Not the correct data type
    with pytest.raises(AccessError):
        users_all(123)

    # Not an authorised user
    bad_token = 'invalid_token'
    with pytest.raises(AccessError):
        users_all(bad_token)

def test_all_standard(create_users):
    users_return = users_all(users[1]['token'])

    # check correct details have been returned
    assert users_return['users'][0]['u_id'] == users[0]['u_id']
    assert users_return['users'][0]['email'] == 'validuseremail@gmail.com'
    assert users_return['users'][0]['name_first'] == 'User'
    assert users_return['users'][0]['name_last'] == 'One'
    assert users_return['users'][0]['handle_str'] == 'userone'

    assert users_return['users'][1]['u_id'] == users[1]['u_id']
    assert users_return['users'][1]['u_id'] == users[1]['u_id']
    assert users_return['users'][1]['email'] == 'validuser2email@gmail.com'
    assert users_return['users'][1]['name_first'] == 'User'
    assert users_return['users'][1]['name_last'] == 'Two'
    assert users_return['users'][1]['handle_str'] == 'usertwo'

    assert users_return['users'][2]['u_id'] == users[2]['u_id']
    assert users_return['users'][2]['email'] == 'validuser3email@gmail.com'
    assert users_return['users'][2]['name_first'] == 'User'
    assert users_return['users'][2]['name_last'] == 'Three'
    assert users_return['users'][2]['handle_str'] == 'userthree'
