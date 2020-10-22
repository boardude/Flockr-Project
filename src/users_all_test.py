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
from helper import get_random_str, get_uid_from_token, register_and_login
from user import user_profile_sethandle
from data import users
from error import AccessError

def test_all_invalid_token():
    clear()
    # register two users
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')

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
    bad_token = get_random_str(6)
    while bad_token is token_1 or bad_token is token_2:
        bad_token = get_random_str(6)

    with pytest.raises(AccessError):
        users_all(bad_token)

def test_all_standard():
    clear()
    # register and change profile details of three users
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    user_profile_sethandle(token_1, 'validuser1')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    user_profile_sethandle(token_2, 'validuser2')
    token_3 = register_and_login('validuser3email@gmail.com', 'validpass3', 'User', 'Three')
    user_profile_sethandle(token_3, 'validuser3')

    # ensure all three tokens work
    users_return = users_all(token_2)

    # check correct details have been returned
    assert users_return['users'][0]['u_id'] == get_uid_from_token(token_1)
    assert users_return['users'][0]['email'] == 'validuseremail@gmail.com'
    assert users_return['users'][0]['name_first'] == 'User'
    assert users_return['users'][0]['name_last'] == 'One'
    assert users_return['users'][0]['handle_str'] == 'validuser1'

    assert users_return['users'][1]['u_id'] == get_uid_from_token(token_2)
    assert users_return['users'][1]['u_id'] == get_uid_from_token(token_2)
    assert users_return['users'][1]['email'] == 'validuser2email@gmail.com'
    assert users_return['users'][1]['name_first'] == 'User'
    assert users_return['users'][1]['name_last'] == 'Two'
    assert users_return['users'][1]['handle_str'] == 'validuser2'

    assert users_return['users'][2]['u_id'] == get_uid_from_token(token_3)
    assert users_return['users'][2]['email'] == 'validuser3email@gmail.com'
    assert users_return['users'][2]['name_first'] == 'User'
    assert users_return['users'][2]['name_last'] == 'Three'
    assert users_return['users'][2]['handle_str'] == 'validuser3'
