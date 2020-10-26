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
from auth import auth_login, auth_register
from error import InputError, AccessError
from other import clear
from data import users
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle

@pytest.fixture
def initial_users():
    clear()
    auth_register('test1@test.com', 'password', 'first_name', 'last_name')
    auth_login('test1@test.com', 'password')
    auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')
    auth_login('test2@test.com', 'password')
    auth_register('test3@test.com', 'password', 'user3_first_name', 'user3_last_name')
    auth_login('test3@test.com', 'password')

def test_user_profile(initial_users):
    '''
        valid test
        register and login user1
        test for accuracy of details of returned details
    '''
    assert user_profile(users[0]['token'], users[0]['u_id'])['user']['u_id'] == users[0]['u_id']
    assert user_profile(users[0]['token'], users[0]['u_id'])['user']['email'] == 'test1@test.com'
    assert user_profile(users[0]['token'], users[0]['u_id'])['user']['name_first'] == 'first_name'
    assert user_profile(users[0]['token'], users[0]['u_id'])['user']['name_last'] == 'last_name'
    assert user_profile(users[0]['token'], users[0]['u_id'])['user']['handle_str'] == 'first_namelast_name'

def test_profile_invalid_uid(initial_users):
    '''
        invalid uid to check
    '''
    with pytest.raises(InputError):
        user_profile(users[0]['token'], 0)

def test_profile_invalid_token(initial_users):
    '''
    test the token does not refer to a valid user
    '''
    with pytest.raises(AccessError):
        user_profile('invalid_token', users[0]['u_id'])

### TEST OF SETNAME ###


def test_valid_setname(initial_users):
    '''
        valid test
        register and login user1
        update the authorised user's first and last name
    '''
    #normal test
    user_profile_setname(users[0]['token'], 'first_name', 'last_name')
    assert user_profile(users[0]['token'], users[0]['u_id'])['user']['name_first'] == 'first_name'
    assert user_profile(users[0]['token'], users[0]['u_id'])['user']['name_last'] == 'last_name'
    # test for length 50
    long_name = '0123456789' * 5
    user_profile_setname(users[1]['token'], long_name, long_name)
    assert user_profile(users[1]['token'], users[1]['u_id'])['user']['name_first'] == long_name
    assert user_profile(users[1]['token'], users[1]['u_id'])['user']['name_last'] == long_name
    #test for length 1
    user_profile_setname(users[2]['token'], '1', '1')
    assert user_profile(users[2]['token'], users[2]['u_id'])['user']['name_first'] == '1'
    assert user_profile(users[2]['token'], users[2]['u_id'])['user']['name_last'] == '1'

def test_setname_invalid_firstname(initial_users):
    '''
        invalid test of 0 characters and 26 characters of firstname
    '''
    long_name = '0123456789' * 5 + '1'
    with pytest.raises(InputError):
        user_profile_setname(users[0]['token'], long_name, 'last_name')
    with pytest.raises(InputError):
        user_profile_setname(users[0]['token'], '', 'last_name')

def test_setname_invalid_lastname(initial_users):
    '''
        invalid test of 0 characters and 26 characters of last name
    '''
    long_name = '0123456789' * 5 + '1'
    with pytest.raises(InputError):
        user_profile_setname(users[0]['token'], 'first_name', long_name)
    with pytest.raises(InputError):
        user_profile_setname(users[0]['token'], 'first_name', '')

def test_setname_invalid_token(initial_users):
    '''
    test the token does not refer to any valid user
    '''
    with pytest.raises(AccessError):
        user_profile_setname('invalid_token', 'new_first_name', 'new_last_name')

###TEST OF SETEMAIL###

def test_profile_setemail_valid(initial_users):
    '''
        valid test for profile setemail
        register and login user
        update the email
    '''
    user_profile_setemail(users[0]['token'], 'testvalid@test.com')
    assert user_profile(users[0]['token'], users[0]['u_id'])['user']['email'] == 'testvalid@test.com'

def test_setemail_invalid_email(initial_users):
    '''
        invalid test for profile setemail
        register and login user
        give an invalid email
    '''
    with pytest.raises(InputError):
        user_profile_setemail(users[0]['token'], 'testvalidtest.com')

def test_setemail_occupied_email(initial_users):
    '''
        invalid test for the profile email being used
        register and login user
        give an used email
    '''
    with pytest.raises(InputError):
        user_profile_setemail(users[0]['token'], 'test2@test.com')

def test_setemail_invalid_token(initial_users):
    '''
    test the token does not refer to a valid user
    '''
    with pytest.raises(AccessError):
        user_profile_setemail('invalid_token', 'newemail@test.com')

###TEST OF SETHANDLE###

def test_sethandle_valid(initial_users):
    '''
        valid test for sethandle
    '''
    #test for normal case
    user_profile_sethandle(users[0]['token'], 'updatename')
    assert user_profile(users[0]['token'], users[0]['u_id'])['user']['handle_str'] == 'updatename'

    #test for length 3
    user_profile_sethandle(users[1]['token'], 'abc')
    assert user_profile(users[1]['token'], users[1]['u_id'])['user']['handle_str'] == 'abc'

    #test for length 20
    user_profile_sethandle(users[2]['token'], '01234567890123456789')
    assert user_profile(users[2]['token'], users[2]['u_id'])['user']['handle_str'] == '01234567890123456789'

def test_sethandle_invalid_length(initial_users):
    '''
        invalid test for the incorrect length:
            1. characters less than 3
            2. characters more than 20
    '''
    with pytest.raises(InputError):
        user_profile_sethandle(users[0]['token'], 'u')
    with pytest.raises(InputError):
        user_profile_sethandle(users[0]['token'], '012345678901234567890')
    with pytest.raises(InputError):
        user_profile_sethandle(users[0]['token'], '')
    with pytest.raises(InputError):
        user_profile_sethandle(users[0]['token'], '12')

def test_sethandle_being_used(initial_users):
    '''
        invalid test for the handle has being used
    '''
    temp1_handle_str = user_profile(users[0]['token'], users[0]['u_id'])['user']['handle_str']
    temp2_handle_str = user_profile(users[1]['token'], users[1]['u_id'])['user']['handle_str']
    with pytest.raises(InputError):
        user_profile_sethandle(users[0]['token'], temp2_handle_str)
    with pytest.raises(InputError):
        user_profile_sethandle(users[1]['token'], temp1_handle_str)

def test_sethandle_invalid_token(initial_users):
    '''
    test the token does not refer to a valid user
    '''
    with pytest.raises(AccessError):
        user_profile_sethandle('invalidtoken', 'newhandle')
