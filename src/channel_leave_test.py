import pytest
import auth
import channel 
from channels import channels_create
from data import users, channels
from error import InputError, AccessError
from other import clear

'''
    chennel_leave_test:
        1. channel_leave() works well (no error) (member leave)
        2. channel_leave() works well (no error) (owner leave)
        2. input error, Channel ID is not a valid channel
        3. access error, Authorised user is not a member of channel with channel_id

    3 help functions:
        1. is_user_in_channel(channel_id, u_id)
            this will check does channel contain the given user or not
        2. is_channel_in_user_data(channel_id, u_id)
            this will check does user's data contain the given channel
        check data.py for more details
        3. is_user_an_owner(channel_id, u_id)
            this will return True if user is a onwer of that channel
            return False if not
'''

def test_channel_leave_member():
    # valid test
    # regiser user1 and user2
    # user1 create a new channel and invite user2
    # then user2 leave the channel
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user2_name')['u_id']
    token_1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    token_2 = auth.auth_login('test2@test.com', 'password')['token']
    channel_id = channels_create(token_1 ,'test_channel', True)['channel_id']
    channel.channel_invite(token_1, channel_id, u2_id)
    channel.channel_leave(token_2, channel_id) 
    assert is_user_in_channel(channel_id, u1_id) is True
    assert is_user_in_channel(channel_id, u2_id) is False
    assert is_channel_in_user_data(channel_id, u1_id) is True
    assert is_channel_in_user_data(channel_id, u2_id) is False

def test_channel_leave_owner():
    # valid test
    # regiser user1 and user2
    # user1 create a new channel and invite user2
    # then user1 leave the channel
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user2_name')['u_id']
    token_1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    token_2 = auth.auth_login('test2@test.com', 'password')['token']
    channel_id = channels_create(token_1 ,'test_channel', True)['channel_id']
    assert is_user_an_owner(channel_id, u1_id) is True
    channel.channel_invite(token_1, channel_id, u2_id)
    channel.channel_leave(token_1, channel_id) 
    assert is_user_in_channel(channel_id, u1_id) is False
    assert is_user_in_channel(channel_id, u2_id) is True
    assert is_channel_in_user_data(channel_id, u1_id) is False
    assert is_channel_in_user_data(channel_id, u2_id) is True
    assert is_user_an_owner(channel_id, u1_id) is False
    assert is_user_an_owner(channel_id, u2_id) is False

def test_leave_InputError_channel():
    #invalid test of channel id is not a valid
    # regiser user1 and user2
    # user1 create a new channel and invite user2
    # then user2 leave channel with wrong channel_id
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_nanme')['u_id']
    token_1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    token_2 = auth.auth_login('test2@test.com', 'password')['token']
    channel_id = channels_create(token_1,'channel_name', True)['channel_id']
    channel.channel_invite(token_1, channel_id, u2_id)
    with pytest.raises(InputError) as e:
        channel.channel_leave(token_2, channel_id + 1)
    assert is_user_in_channel(channel_id, u1_id) is True
    assert is_user_in_channel(channel_id, u2_id) is True
    assert is_channel_in_user_data(channel_id, u1_id) is True
    assert is_channel_in_user_data(channel_id, u2_id) is True

def test_leave_AccessError_not_authorised_member():
    #invalid test of the authorised user is not already a member of t he channel
    # register user1 and user2
    # user1 create a new channel and DO NOT invite user2
    # user2 leave channel with user1's channel_id
    clear()
    u1_id = auth.auth_register('test1@test.com', 'password', 'user1_name', 'user1_name')['u_id']
    token_1 = auth.auth_login('test1@test.com', 'password')['token']
    u2_id = auth.auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')['u_id']
    token_2 = auth.auth_login('test2@test.com', 'password')['token']
    channel_id = channels_create(token_1,'channel_name', True)['channel_id']
    with pytest.raises(AccessError) as e:
        channel.channel_leave(token_2, channel_id)
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
        if channel['channel_id'] == channel_id:
            all_members = channel.get('all_members')
    for member in all_members:
        if member == u_id:
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

def is_user_an_owner(channel_id, u_id):
    for channel in channels:
        if channel['channel_id'] == channel_id:
            owners = channel['owner_members']
    for owner in owners:
        if owner == u_id:
            return True
    return False