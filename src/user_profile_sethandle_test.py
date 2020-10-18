'''
    test of user_profile_sethandle
        1.valid test for sethandle
        2.incorrect handle length
        3.handle being used
'''


import pytest
import auth
from error import InputError
from other import clear
from user import user_profile, user_profile_sethandle

def test_handle_valid():
    '''
        valid test for sethandle
    '''
    clear()
    u_id = auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')
    user_profile_sethandle(token, 'updatename')
    assert user_profile(token, u_id)['handle'] == 'updatename'
def test_handle_incorrect_length():
    '''
        invalid test for the incorrect length:
            1. characters less than 3
            2. characters more than 20
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')
    with pytest.raises(InputError):
        user_profile_sethandle(token, 'u')
    with pytest.raises(InputError):
        user_profile_sethandle(token, 'abcdefghijklmnopkistuvwxyz')
def test_handle_beingused():
    '''
        invalid test for the handle has being used
    '''
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token1 = auth.auth_login('test1@test.com', 'password')
    auth.auth_register('test2@test.com', 'password', 'user2_first_name', 'user2_last_name')
    auth.auth_login('test2@test.com', 'password')
    temp = user_profile(token1, u1_id)['handle_str']
    with pytest.raises(InputError):
        user_profile_sethandle(token1, temp)
 