'''
import pytest for testing
import auth and channel for manipulating user and channel
import other for clearing data
import error for raising errors
'''
import pytest
import channel
from channels import  channels_create
from other import clear
import auth
from error import InputError, AccessError

def test_valid():
    '''
    nothing here because we need message_send() function
    implement this test in iteration 2
    '''

def test_input_error_invalid_channel():
    '''
    this test is for checking input error when Channel ID is not a valid channel
    steps:
        register user1 and create a new channel
        user1 requests channel_messages with wrong channel_id
    '''
    clear()
    token = auth.auth_register('test1@test.com', 'test123', 'test', 'test')['token']
    auth.auth_login('test1@test.com', 'test123')
    channel_id = channels_create(token, 'test_channel', True)['channel_id']
    with pytest.raises(InputError):
        assert channel.channel_messages(token, channel_id + 1, 0)
    # should raise an input error since (channel_id - 1) does not exist

def test_input_error_invalid_start():
    '''
    this test is for checking input error when start is greater than
    the total number of messages in the channel
    steps:
        register user1 and create a new channel
        user1 requests channel_messages with an invalid start
    '''
    clear()
    token = auth.auth_register('test1@test.com', 'test123', 'test', 'test')['token']
    auth.auth_login('test1@test.com', 'test123')
    channel_id = channels_create(token, 'test_channel', True)['channel_id']
    with pytest.raises(InputError):
        assert channel.channel_messages(token, channel_id, 1)

def test_access_error_not_member():
    '''
    this test is for checking access error when Authorised user is not
    a member of channel with channel_id
    steps:
        register user1 and user2
        user1 create a new channel
        user2 requests channel_messages
    # need message.py finished
    clear()
    token_1 = auth.auth_register('test1@test.com', 'test123', 'test', 'test')['token']
    auth.auth_login('test1@test.com', 'test123')
    token_2 = auth.auth_register('test2@test.com', 'test123', 'test', 'test')['token']
    auth.auth_login('test2@test.com', 'test123')
    channel_id = channels_create(token_1, 'test_channel', True)['channel_id']
    with pytest.raises(AccessError) as e:
        assert channel.channel_messages(token_2, channel_id, 0)
    '''

def test_access_error_not_valid_token():
    '''
    this test is for checking if the token does not refer to a valid user
    '''
    clear()
    token_1 = auth.auth_register('test1@test.com', 'test123', 'test', 'test')['token']
    auth.auth_login('test1@test.com', 'test123')
    channel_id = channels_create(token_1, 'test_channel', True)['channel_id']
    with pytest.raises(AccessError):
        assert channel.channel_messages('invalid_token', channel_id, 0)
