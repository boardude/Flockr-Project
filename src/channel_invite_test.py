import pytest
import auth
import channel 
from channels import channels_create
from data import users, channels
from error import InputError, AccessError
from other import clear

'''
    channel_invite_test:
        1. channel_invite() works well (no error)
        2. input error, Channel ID is not a valid channel
        3. input error, u_id does not refer to a valid user
        4. access error, the authorised user is not already a member of the channel
    
    2 help functions:
        1. is_user_in_channel(channel_id, u_id)
            this will check does channel contain the given user or not
        2. is_channel_in_user_data(channel_id, u_id)
            this will check does user's data contain the given channel
        check data.py for more details
'''

def test_channel_invite():
    #valid test
    #register user1 and user2
    #user1 create a channel and invite user2
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    auth.auth_login('test2@test.com', 'password')
    channel_id = channels_create(token ,'channel_name', True)['c_id']
    channel.channel_invite(token, channel_id, u2_id) 
    assert is_user_in_channel(channel_id, u1_id) is True
    assert is_user_in_channel(channel_id, u2_id) is True
    assert is_channel_in_user_data(channel_id, u1_id) is True
    assert is_channel_in_user_data(channel_id, u2_id) is True
    

def test_invite_InputError_invalid_channel():
    #invalid test of worng channel id
    # register user1 and user2
    # user1 create a new channel and invite user2 with a wrong channel_id
    clear()
    auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')
    token = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    auth.auth_login('test2@test.com', 'password')
    channel_id = channels_create(token,'channel_name', True)['channel_id']
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(token, channel_id + 1, u2_id)
    assert is_user_in_channel(channel_id, u2_id) is False
    assert is_channel_in_user_data(channel_id, u2_id) is False


def test_invite_InputError_invalid_u_id():
    #invalid test of invalid u_id
    # register user1
    # user1 create a new channel and use correct channel_id to 
    # invite another user which is not exist
    clear()
    u_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token = auth.auth_login('test1@test.com', 'password')['token']
    channel_id = channels_create(token, 'channel_name', True)['c_id']
    with pytest.raises(InputError) as e:
        channel.channel_invite(token, channel_id, u_id + 1)


def test_invite_AccessError_not_authorised_member():
    #invalid test of the authorised user is not already a member of t he channel
    # register user1, user2 and user3
    # user1 create a new channel, and user2 invite user3
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token_1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    token_2 = auth.auth_login('test2@test.com', 'password')['token']
    u3_id = auth.auth_register('test3@test.com', 'password', 'user3_name', 'user3_name')['u_id']
    auth.auth_login('test3@test.com', 'password')
    channel_id = channels_create(token_1, 'channel_name', True)['c_id'] 
    with pytest.raises(AccessError) as e:
        channel.channel_invite(token_2, channel_id, u3_id)
    assert is_user_in_channel(channel_id, u1_id) is True
    assert is_user_in_channel(channel_id, u2_id) is False
    assert is_user_in_channel(channel_id, u3_id) is False
    assert is_channel_in_user_data(channel_id, u1_id) is True
    assert is_channel_in_user_data(channel_id, u2_id) is False
    assert is_channel_in_user_data(channel_id, u3_id) is False


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
    