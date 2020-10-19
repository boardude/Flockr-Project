'''
    test for user/profile:
        1.valid test for profile
        2.invalid test for uid
        3.invalid test for token

    test of user/profile/setname
        1.valid test
        2.name_first is not between 1 and 50 characters inclusively in length
        3.name_last is not between 1 and 50 characters inclusively in length

    test of user/profile/setemail
        1.valid test for setemail
        2.invalid email for setemail test
        3.invalid token for setemail test

    test of user/prifile/sethandle
        1.valid test for sethandle
        2.incorrect handle length
        3.handle being

    test of invalid token
'''
import pytest
import auth
from error import InputError, AccessError
from other import clear
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle

def test_user_profile():
    '''
        valid test
        register and login user1
        test for accuracy of details of returned details
    '''
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token = auth.auth_login('test1@test.com', 'password')['token']

    assert user_profile(token, u1_id)['user']['u_id'] == u1_id
    assert user_profile(token, u1_id)['user']['email'] == 'test1@test.com'
    assert user_profile(token, u1_id)['user']['name_first'] == 'user1_name'
    assert user_profile(token, u1_id)['user']['name_last'] == 'user1_name'
    assert user_profile(token, u1_id)['user']['handle_str'] == 'user1_nameuser1_name'

def test_invalid_uid():
    '''
        invalid uid to check
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')
    token1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    auth.auth_login('test2@test.com', 'password')
    with pytest.raises(InputError):
        user_profile(token1, u2_id)


### TEST OF SETNAME ###


def test_valid_setname():
    '''
        valid test
        register and login user1
        update the authorised user's first and last name
    '''
    clear()
    #normal test
    u1_id = auth.auth_register('test1@test.com', 'password',
                               'user1_first_name', 'user1_last_name')['u_id']
    token1 = auth.auth_login('test1@test.com', 'password')['token']
    user_profile_setname(token1, 'first_name', 'last_name')
    assert user_profile(token1, u1_id)['user']['name_first'] == 'first_name'
    assert user_profile(token1, u1_id)['user']['name_last'] == 'last_name'
    # test for length 50
    u2_id = auth.auth_register('test2@test.com', 'password',
                               'user2_first_name', 'user2_last_name')['u_id']
    token2 = auth.auth_login('test2@test.com', 'password')['token']
    long_name = '0123456789'
    long_name = long_name * 5
    user_profile_setname(token2, long_name, long_name)
    assert user_profile(token2, u2_id)['user']['name_first'] == long_name
    assert user_profile(token2, u2_id)['user']['name_last'] == long_name
    #test for length 1
    u3_id = auth.auth_register('test3@test.com', 'password',
                               'user3_first_name', 'user3_last_name')['u_id']
    token3 = auth.auth_login('test3@test.com', 'password')['token']
    user_profile_setname(token3, '1', '1')
    assert user_profile(token3, u3_id)['user']['name_first'] == '1'
    assert user_profile(token3, u3_id)['user']['name_last'] == '1'

def test_invalid_firstname():
    '''
        invalid test of 0 characters and 26 characters of firstname
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')['token']
    long_name = '012345678910'
    long_name = long_name * 5
    with pytest.raises(InputError):
        user_profile_setname(token, long_name, 'last_name')
    with pytest.raises(InputError):
        user_profile_setname(token, '', 'last_name')

def test_invalid_lastname():
    '''
        invalid test of 0 characters and 26 characters of last name
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')['token']
    long_name = '012345678910'
    long_name = long_name * 5
    with pytest.raises(InputError):
        user_profile_setname(token, 'first_name', long_name)
    with pytest.raises(InputError):
        user_profile_setname(token, 'first_name', '')


###TEST OF SETEMAIL###

def test_profile_setemail_valid():
    '''
        #valid test for profile setemail
        #register and login user
        #update the email
    '''
    clear()
    u_id = auth.auth_register('test1@test.com', 'password',
                              'user1_first_name', 'user1_last_name')['u_id']
    token = auth.auth_login('test1@test.com', 'password')['token']
    user_profile_setemail(token, 'testvalid@test.com')
    assert user_profile(token, u_id)['user']['email'] == 'testvalid@test.com'

def test_profile_setemail_incorrect_format():
    '''
        #invalid test for profile setemail
        #register and login user
        #give an invalid email
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')['token']

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
    token1 = auth.auth_login('test1@test.com', 'password')['token']
    auth.auth_register('test2@test.com', 'password', 'user2_first_name', 'user2_last_name')
    auth.auth_login('test2@test.com', 'password')
    with pytest.raises(InputError):
        user_profile_setemail(token1, 'test2@test.com')


###TEST OF SETHANDLE###

def test_handle_valid():
    '''
        valid test for sethandle
    '''
    clear()
    #test for normal case
    u1_id = auth.auth_register('test1@test.com', 'password',
                               'user1_first_name', 'user1_last_name')['u_id']
    token1 = auth.auth_login('test1@test.com', 'password')['token']
    user_profile_sethandle(token1, 'updatename')
    assert user_profile(token1, u1_id)['user']['handle_str'] == 'updatename'

    #test for length 3
    u2_id = auth.auth_register('test2@test.com', 'password',
                               'user2_first_name', 'user2_last_name')['u_id']
    token2 = auth.auth_login('test2@test.com', 'password')['token']
    user_profile_sethandle(token2, 'abc')
    assert user_profile(token2, u2_id)['user']['handle_str'] == 'abc'

    #test for length 20
    u3_id = auth.auth_register('test3@test.com', 'password',
                               'user3_first_name', 'user3_last_name')['u_id']
    token3 = auth.auth_login('test3@test.com', 'password')['token']
    user_profile_sethandle(token3, '12345678911234567891')
    assert user_profile(token3, u3_id)['user']['handle_str'] == '12345678911234567891'

def test_handle_incorrect_length():
    '''
        invalid test for the incorrect length:
            1. characters less than 3
            2. characters more than 20
    '''
    clear()
    auth.auth_register('test1@test.com', 'password',
                       'user1_first_name', 'user1_last_name')
    token = auth.auth_login('test1@test.com', 'password')['token']
    with pytest.raises(InputError):
        user_profile_sethandle(token, 'u')
    with pytest.raises(InputError):
        user_profile_sethandle(token, 'abcdefghijklmnopkistuvwxyz')
    with pytest.raises(InputError):
        user_profile_sethandle(token, '')
    with pytest.raises(InputError):
        user_profile_sethandle(token, '12')

def test_handle_being_used():
    '''
        invalid test for the handle has being used
    '''
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password',
                               'user1_first_name', 'user1_last_name')['u_id']
    token1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password',
                               'user2_first_name', 'user2_last_name')['u_id']
    token2 = auth.auth_login('test2@test.com', 'password')['token']
    temp1_handle_str = user_profile(token1, u1_id)['user']['handle_str']
    temp2_handle_str = user_profile(token2, u2_id)['user']['handle_str']
    with pytest.raises(InputError):
        user_profile_sethandle(token1, temp2_handle_str)
    with pytest.raises(InputError):
        user_profile_sethandle(token2, temp1_handle_str)


### ACCESSERROR ###
def test_invalid_token():
    '''
        invalid token to check
    '''
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    auth.auth_login('test1@test.com', 'password')
    with pytest.raises(AccessError):
        user_profile('invalidtoken', u1_id)
