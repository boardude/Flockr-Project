# Yicheng (Mike) Zhu
# Last updated 22/10/2020

import pytest
from data import users
from other import admin_userpermission_change, clear
from channels import channels_create
from auth import auth_register, auth_login
from helper import get_user_from_token
from error import InputError, AccessError

@pytest.fixture
def create_users():
    clear()
    auth_register('validuseremail@gmail.com', 'validpass', 'User', 'One')
    auth_register('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    auth_register('validuser3email@gmail.com', 'validpass3', 'User', 'Three')
    auth_login('validuseremail@gmail.com', 'validpass')
    auth_login('validuser2email@gmail.com', 'validpass2')
    auth_login('validuser3email@gmail.com', 'validpass3')

def test_userpermission_InputError(create_users):
    # u_id does not refer to a valid user
    with pytest.raises(InputError):
        admin_userpermission_change(users[0]['token'], 0, 1)

    # permission_id does not refer to a value permission
    with pytest.raises(InputError):
        admin_userpermission_change(users[0]['token'], users[1]['u_id'], 3)

    # permission_id does not refer to a value permission (wrong data type)
    with pytest.raises(InputError):
        admin_userpermission_change(users[0]['token'], users[1]['u_id'], 'str')

def test_userpermission_AccessError(create_users):
    # token is not an authorised user
    with pytest.raises(AccessError):
        admin_userpermission_change('invalid_token', users[0]['u_id'], 2)

    # token is an authorised user but not an owner
    with pytest.raises(AccessError):
        admin_userpermission_change(users[1]['token'], users[0]['u_id'], 2)

def test_userpermission_standard(create_users):
    # preliminary assertions
    assert users[0]['permission_id'] == 1
    assert users[1]['permission_id'] == 2
    assert users[2]['permission_id'] == 2

    # testing
    admin_userpermission_change(users[0]['token'], users[1]['u_id'], 1)
    assert users[1]['permission_id'] == 1

    admin_userpermission_change(users[0]['token'], users[2]['u_id'], 1)
    assert users[2]['permission_id'] == 1   
   
    admin_userpermission_change(users[1]['token'], users[2]['u_id'], 2)
    assert users[2]['permission_id'] == 2

    admin_userpermission_change(users[1]['token'], users[0]['u_id'], 2)
    assert users[0]['permission_id'] == 2
