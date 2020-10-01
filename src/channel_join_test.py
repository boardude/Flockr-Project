import pytest
import auth
import channel 
from channels import channels_create
from data import users, channels
from error import InputError, AccessError
from other import clear

'''
    channel_join_test:
        !!!!! if the token does not refer to a valid user, program will ignore the request,
        check assumption.md for more details

        1. channel_join() works well (no error)
        2. input error, Channel ID is not a valid channel
        3. access error, channel_id refers to a channel that is private 
            (when the authorised user is not a global owner)
    
    2 help functions:
        1. is_user_in_channel(channel_id, u_id)
            this will check does channel contain the given user or not
        2. is_channel_in_user_data(channel_id, u_id)
            this will check does user's data contain the given channel
        check data.py for more details
'''

def test_channel_join():
    #valid test
    # register user1 and user2
    # user1 create a public channel
    # user2 join that channel
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token_1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    token_2 = auth.auth_login('test2@test.com', 'password')['token']
    channel_id = channels_create(token_1 ,'channel_name', True)['c_id']
    assert channel.channel_join(token_2, channel_id) 
    assert is_user_in_channel(channel_id, u1_id) is True
    assert is_user_in_channel(channel_id, u2_id) is True
    assert is_channel_in_user_data(channel_id, u1_id) is True
    assert is_channel_in_user_data(channel_id, u2_id) is True


def test_join_InputError_channel():
    #invalid test of the invalid channel ID
    # register user1 and user2
    # user1 create a public channel
    # user2 join channel with wrong channel_id
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token_1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    token_2 = auth.auth_login('test2@test.com', 'password')['token']
    channel_id = channels_create(token_1 ,'channel_name', True)['c_id']
    with pytest.raises(InputError) as e:
        channel.channel_join(token_2, channel_id + 1)
    assert is_user_in_channel(channel_id, u1_id) is True
    assert is_user_in_channel(channel_id, u2_id) is False
    assert is_channel_in_user_data(channel_id, u1_id) is True
    assert is_channel_in_user_data(channel_id, u2_id) is False


def test_join_AccessError_channel():
    #invalid test of the private channel
    # register user1 and user2
    # user1 create a NOT-public channel
    # user2 join that channel
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token_1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    token_2 = auth.auth_login('test2@test.com', 'password')['token']
    channel_id = channels_create(token_1 ,'channel_name', False)['c_id']
    with pytest.raises(AccessError) as e:
        channel.channel_join(token_2, channel_id)
    assert is_user_in_channel(channel_id, u1_id) is True
    assert is_user_in_channel(channel_id, u2_id) is False
    assert is_channel_in_user_data(channel_id, u1_id) is True
    assert is_channel_in_user_data(channel_id, u2_id) is False


### help function

### check a given user is in the given channel or not
### retrun true if the user is in channel's list
###     else return false
def is_user_in_channel(channel_id, u_id):
    for channel in channels:
        if channel['c_id'] == channel_id:
            all_members = channel.get('all_members')
    for member in all_members:
        if member['u_id'] == u_id:
            return True
    return False
    
### check a given channel is in the given user or not
### return true if the channel is in user's list
###     else return false
def is_channel_in_user_data(channel_id, u_id):
    for user in users:
        if user['u_id'] == u_id:
            for channel in user['channels']:
                if channel == channel_id:
                    return True
    return False
    