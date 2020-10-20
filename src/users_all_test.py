"""
    random and string modules allow for random string generation
    for test_*_invalid_token tests

    pytest module allows us to test if exceptions are thrown at appropriate times

    other module contains user_all function that we need to test, as well as useful
    helper functions

    data module contains data on users stored in a "users" list

    error module defines an AccessError exception that is to be thrown when
    an invalid token is passed
"""

import random
import string
import pytest
from other import users_all, register_and_login, clear
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
    bad_token = get_random_string(6)
    while bad_token is token_1 or bad_token is token_2:
        bad_token = get_random_string(6)

    with pytest.raises(AccessError):
        users_all(bad_token)

def test_all_standard():
    clear()
    # register and change profile details of three users
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    token_3 = register_and_login('validuser3email@gmail.com', 'validpass3', 'User', 'Three')

    # ensure all three tokens work
    users_return_1 = users_all(token_1)
    users_return_2 = users_all(token_2)
    users_return_3 = users_all(token_3)

    # check correct details have been returned
    check_user_profiles(users_return_1, 3)
    check_user_profiles(users_return_2, 3)
    check_users_profile(users_return_3, 3)


############### HELPER FUNCTIONS ################
def check_user_profiles(profiles, num_users):
    for i in range(num_users):
        assert profiles[i]['u_id'] == users[i]['u_id']
        assert profiles[i]['email'] == users[i]['email']
        assert profiles[i]['name_first'] == users[i]['name_first']
        assert profiles[i]['name_last'] == users[i]['name_last']
        assert profiles[i]['handle_str'] == users[i]['handle']
