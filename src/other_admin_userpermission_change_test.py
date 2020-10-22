# Yicheng (Mike) Zhu
# Last updated 22/10/2020

import pytest
import random
from other import admin_userpermission_change, clear
from channels import channels_create
from helper import register_and_login, get_random_str, get_user_from_token_naive
from error import InputError, AccessError

def test_userpermission_InputError():
    clear()
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    user_1 = get_user_from_token_naive(token_1)
    user_2 = get_user_from_token_naive(token_2)

    # u_id does not refer to a valid user
    with pytest.raises(InputError):
        bad_id = random.randint(0, 999)
        while bad_id is user_1['u_id'] or bad_id is user_2['u_id']:
            bad_id = random.randint(0, 999)
        admin_userpermission_change(token_1, bad_id, 1)

    # permission_id does not refer to a value permission
    with pytest.raises(InputError):
        admin_userpermission_change(token_1, user_2['u_id'], 3)

    # permission_id does not refer to a value permission (wrong data type)
    with pytest.raises(InputError):
        admin_userpermission_change(token_1, user_2['u_id'], 'str')

def test_userpermission_AccessError():
    clear()
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    user_1 = get_user_from_token_naive(token_1)

    # token is not an authorised user
    with pytest.raises(AccessError):
        bad_token = get_random_str(6)
        while bad_token is token_1 or bad_token is token_2:
            bad_token = get_random_str(6)
        admin_userpermission_change(bad_token, user_1['u_id'], 2)

    # token is an authorised user but not an owner
    with pytest.raises(AccessError):
        admin_userpermission_change(token_2, user_1['u_id'], 2)

def test_userpermission_standard():
    clear()
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    token_3 = register_and_login('validuser3email@gmail.com', 'validpass3', 'User', 'Three')
    user_1 = get_user_from_token_naive(token_1)
    user_2 = get_user_from_token_naive(token_2)
    user_3 = get_user_from_token_naive(token_3)

    # preliminary assertions
    assert user_1['permission_id'] == 1
    assert user_2['permission_id'] == 2
    assert user_3['permission_id'] == 2

    # testing
    admin_userpermission_change(token_1, user_2['u_id'], 1)
    assert user_2['permission_id'] == 1

    admin_userpermission_change(token_1, user_3['u_id'], 1)
    assert user_3['permission_id'] == 1   
   
    admin_userpermission_change(token_2, user_3['u_id'], 2)
    assert user_3['permission_id'] == 2

    admin_userpermission_change(token_2, user_1['u_id'], 2)
    assert user_1['permission_id'] == 2
