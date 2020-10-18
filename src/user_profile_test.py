'''
    test for user/profile:
        1.valid test for profile
        2.invalid test for uid
        3.invalid test for token
'''
import pytest
import auth
from error import InputError
from other import clear
from user import user_profile

def test_user_profile():
    '''
        #valid test
        #register and login user1
        #test for accuracy of details of returned details
    '''
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token = auth.auth_login('test1@test.com', 'password')
    temp = user_profile(token, u1_id)
    assert isinstance(temp, dict) is True
    assert user_profile(token, u1_id)['u_id'] == u1_id
    assert user_profile(token, u1_id)['email'] == 'test1@test.com'
    assert user_profile(token, u1_id)['name_first'] == 'user1_name'
    assert user_profile(token, u1_id)['name_last'] == 'user1_name'
    assert user_profile(token, u1_id)['handle'] == 'user1_nameuser1_name'
def test_invalid_uid():
    '''
        #invalid uid to check
    '''
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token = auth.auth_login('test1@test.com', 'password')
    with pytest.raises(InputError):
        user_profile(token, u1_id + 1)
def test_invalid_token():
    '''
        #invalid token to check
    '''
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token = auth.auth_login('test1@test.com', 'password')
    with pytest.raises(InputError):
        user_profile(token + 1, u1_id)
