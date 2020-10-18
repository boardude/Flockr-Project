'''
    test of user/profile/setname
        1.valid test
        2.name_first is not between 1 and 50 characters inclusively in length
        3.name_last is not between 1 and 50 characters inclusively in length
'''
import pytest
import auth
from error import InputError
from other import clear
from user import user_profile_setname

def test_valid_setname():
    '''
        # valid test
        # register and login user1
        # update the authorised user's first and last name
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')
    assert user_profile_setname(token, 'first_name', 'last_name')['name_first'] == 'first_name'
    assert user_profile_setname(token, 'first_name', 'last_name')['name_last'] == 'last_name'

def test_invalid_firstname():
    '''
    #invalid test of 0 characters and 26 characters of firstname
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')
    with pytest.raises(InputError):
        user_profile_setname(token, 'abcdefghijklmnopqrstuvwxyz', 'last_name')
    with pytest.raises(InputError):
        user_profile_setname(token, '', 'last_name')
def test_invalid_lastname():
    '''
    #invalid test of 0 characters and 26 characters of last name
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')
    with pytest.raises(InputError):
        user_profile_setname(token, 'first_name', 'abcdefghijklmnopqrstuvwxyz')
    with pytest.raises(InputError):
        user_profile_setname(token, 'first_name', '')
