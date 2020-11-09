'''Tests:
        start:
            1.invalid channel id
            2.an active standup is runnign
        active:
            1.invalid channel id
        send:
            1.invalid channel id
            2.message is more than 1000 characters
            3.standup is not active
            4.the authorised user is not a member in the channel
'''
import pytest
import standup
from datetime import datetime
from other import clear
from channels import channels_create
from error import InputError, AccessError
from data import users
from standup import standup_start, standup_active, standup_send

@pytest.fixture
def initial_users():
    clear()
    token1 = auth_register('test1@test.com', 'password', 'first_name', 'last_name')
    auth_login('test1@test.com', 'password')
    token2 = auth_register('test2@test.com', 'password', 'user2_name', 'user2_name')
    auth_login('test2@test.com', 'password')
    auth_register('test3@test.com', 'password', 'user3_first_name', 'user3_last_name')
    auth_login('test3@test.com', 'password')


def test_start():
    '''
        valid test
        1. register and login user
        2. create channel
        3. start a standup
    '''

    channel_id = channels_create(token1, 'newchannel', True)
    assert standup_start(token1, channel_id, 100) == datetime.now().second + 100

def test_start_invalid_channel_id():
    '''
        invalid test
        1. create a channel
        2. start a standup
    '''
    channel_id = channels_create(token1, 'newchannel', True)
    with pytest.raises(InputError):
        standup_start(token1, channel_id + 1, 100)
    
def test_start_invalid_is_running():
    '''
        invalid test
        1. create a channel
        2. start a standup
        3. start another strandup
    '''
    channel_id = channels_create(token1, 'newchannel', True)
    assert standup_start(token1, channel_id, 100)['time_finish'] == datetime.now().second + 100
    with pytest.raises(InputError):
        standup_start(token1, channel_id, 100)

def test_active():
    '''
        valid test
        1.create a channel
        2.start a standup
        3.get the time_finish and is_active
    '''
    channel_id = channels_create(token1, 'newchannel', True)
    standup_start(token1, channel_id, 100)
    assert standup_active(token1, channel_id)['is_active'] == True
    assert standup_active(token1, channel_id)['time_finish'] == datetime.now().second + 100

def test_active_invalid_channel_id():
    '''
        invalid test
        1. create a channel
        2. start a standup with invalid channel id
    '''
    channel_id = channels_create(token1, 'newchannel', True)
    standup_start(token1, channel_id, 100)
    with pytest.raises(InputError):
        standup_active(token1, channel_id + 1)

def test_send():
    '''
        valid test
        1. create a channel
        2. start a standup
        3. send message
    '''
    channel_id = channels_create(token1, 'newchannel', True)
    ##standup_start(token1, channel_id, 100)### unfinished ###

def test_send_invalid_channel_id():
    '''
        invalid test
        1. invalid channel id
    '''
    channel_id = channels_create(token1, 'newchannel', True)
    with pytest.raises(InputError):
        standup_send(token1, channel_id + 1, 'new_msg')

def test_send_invalid_message():
    '''
        invalid test
        1. invalid message send
    '''
    channel_id = channels_create(token1, 'newchannel', True)
    with pytest.raises(InputError):
        standup_start(token1, channel_id, 'i' * 1001)

def test_send_invalid_is_not_running():
    '''
        invalid test
        1. create a channel
        2. standuup is not currently running
        3. send message
    '''
    channel_id = channels_create(token1, 'newchannel', True)
    assert standup_active(token1, channel_id)['is_active'] == False
    with pytest.raises(InputError):
        standup_send(token1, channel_id, 'new_meg')
    
def test_send_invalid_not_a_menmber_of_channel():
    '''
        invalid test
        1.create a channel
        2.start standup
        3.user2 send a message who is not a member of the known channel
    '''
    channel_id = channels_create(token1, 'newchannel', True)
    standup_start(token1, channel_id, 100)
    with pytest.raises(InputError):
        standup_send(token2, channel_id, 'new_meg')
