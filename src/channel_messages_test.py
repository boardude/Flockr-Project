import pytest
import auth
import channel
from error import InputError, AccessError
from channels import  channels_create
from other import clear

'''
    unfinished version, we need message_send() in iteration
    this test will mainly test errors
    test:
        1. (cannot test now) channel_messages() works well
        2. input error when Channel ID is not a valid channel
        3. input error when start is greater than the total number of messages in the channel
        4. (cannot test now) access error when Authorised user 
            is not a member of channel with channel_id

'''

def test_valid():
    # nothing here because we need message_send() function
    # implement this test in iteration 2
    pass

def test_input_error_channelID():
    # input error when Channel ID is not a valid channel

    # register user1 and create a new channel
    # user1 requests channel_messages with wrong channel_id
    clear()
    token = auth.auth_register('test1@test.com', 'test123', 'test', 'test')['token']
    auth.auth_login('test1@test.com', 'test123')
    channel_id = channels_create(token, 'test_channel', True)['channel_id']
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(token, channel_id + 1, 0)
    # should raise an input error since (channel_id - 1) does not exist

def test_input_error_invalid_start():
    # input error when start is greater than 
    # the total number of messages in the channel

    # register user1 and create a new channel
    # user1 requests channel_messages with an invalid start
    clear()
    token = auth.auth_register('test1@test.com', 'test123', 'test', 'test')['token']
    auth.auth_login('test1@test.com', 'test123')
    channel_id = channels_create(token, 'test_channel', True)['channel_id']
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(token, channel_id, 1)

def test_access_error():
    # access error when Authorised user is not 
    # a member of channel with channel_id

    # register user1 and user2
    # user1 create a new channel
    # user2 requests channel_messages
    '''
    clear()
    token_1 = auth.auth_register('test1@test.com', 'test123', 'test', 'test')['token']
    auth.auth_login('test1@test.com', 'test123')
    token_2 = auth.auth_register('test2@test.com', 'test123', 'test', 'test')['token']
    auth.auth_login('test2@test.com', 'test123')
    channel_id = channels_create(token_1, 'test_channel', True)['channel_id']
    with pytest.raises(AccessError) as e:
        assert channel.channel_messages(token_2, channel_id, 0)
    '''
    