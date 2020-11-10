import pytest
import time
from other import clear
from channels import channels_create
from error import InputError, AccessError
from data import users, channels
from standup import standup_start, standup_active, standup_send
from auth import auth_register, auth_login, token_generate
from channel import channel_join

@pytest.fixture
def initial_data():
    '''
    register 3 users and user 1 and user 3 create a channel
    user2 join channel1
    '''
    clear()
    auth_register('test1@test.com', 'password', 'user1', 'user1')
    auth_login('test1@test.com', 'password')
    auth_register('test2@test.com', 'password', 'user2', 'user2')
    auth_login('test2@test.com', 'password')
    auth_register('test3@test.com', 'password', 'user3', 'user3')
    auth_login('test3@test.com', 'password')
    channel_id_1 = channels_create(users[0]['token'], 'channel_1', True)
    channel_id_2 = channels_create(users[2]['token'], 'channel_1', True)
    channel_join(users[1]['token'], channel_id_1)

########################################
############# start tests ##############
########################################
# 1. standard test
# 2. access error when given token is invalid
# 3. input error when given channal_id is invalid
# 4. input error when channel has already started

def test_start_standard(initial_data):
    '''
    standard test without errors
    user 1 call standup_start in channel 1 and standup lasts 1 second
    check current time is not equal to finish_time
    curr_time add 1 second would be equal to finish_time
    '''
    curr_time = int(time.time())
    finish_time = standup_start(users[0]['token'], channels[0]['channel_id'], 1)['time_finish']
    assert curr_time != finish_time
    assert curr_time + 1 == finish_time

def test_start_error_invalid_token(initial_data):
    '''
    error test when given token is invalid
    1. non-existing
    2. logout token
    '''
    # 1. non-existing token
    with pytest.raises(AccessError):
        standup_start('invalid-token', channels[0]['channel_id'], 1)
    # 2. user1 logout token
    with pytest.raises(AccessError):
        standup_start(token_generate(0, 'logout'), channels[0]['channel_id'], 1)

def test_start_error_invalid_channel(initial_data):
    '''
    error test when given channel_id is invalid
    1. channel_id does not exist
    2. user is not in this channel
    '''
    # 1. non-existing channel with id 0
    with pytest.raises(InputError):
        standup_start(users[0]['token'], 0, 1)
    # 2. user 1 calls standup_start in channel_2
    with pytest.raises(InputError):
        standup_start(users[0]['token'], channels[1]['channel_id'], 1)

def test_start_error_invalid_req(initial_data):
    '''
    error test when user calls standup_start when it is active in that channel
    user 1 calls standup_start in channel_1 and call start again
    '''
    standup_start(users[0]['token'], channels[0]['channel_id'], 3)
    with pytest.raises(InputError):
        standup_start(users[0]['token'], channels[0]['channel_id'], 3)