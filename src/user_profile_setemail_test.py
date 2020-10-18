'''
    setemail test
        1.valid test for setemail
        2.invalid email for setemail test
        3.invalid token for setemail test
'''

import pytest
import auth
from user import user_profile_setemail, user_profile
from error import InputError
from other import clear


def test_profile_setemail_valid():
    '''
        #valid test for profile setemail
        #register and login user
        #update the email
    '''
    clear()
    u_id = auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')
    user_profile_setemail(token, 'testvalid@test.com')

    assert user_profile(token, u_id)['email'] == 'testvalid@test.com'
def test_profile_setemail_invalid():
    '''
        #invalid test for profile setemail
        #register and login user
        #give an invalid email
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')

    with pytest.raises(InputError):
        user_profile_setemail(token, 'testvalidtest.com')
def test_profile_setemail_being_used():
    '''
        #invalid test for the profile email being used
        #register and login user
        #give an used email
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token1 = auth.auth_login('test1@test.com', 'password')
    auth.auth_register('test2@test.com', 'password', 'user2_first_name', 'user2_last_name')
    auth.auth_login('test2@test.com', 'password')
    with pytest.raises(InputError):
        user_profile_setemail(token1, 'test2@test.com')
