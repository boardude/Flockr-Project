''' Test file for message.py '''

import pytest
import auth
from other import clear
from error import InputError, AccessError
from message import message_send, message_edit, message_remove, message_send_later, message_react, message_unreact, message_pin, message_unpin
from data import channels, users
from channels import channels_create
from channel import channel_join
import time

@pytest.fixture
def initial_data():
    '''
    it is a fixture for tests.
    create user 1, user 2 and user 3
    user 1 creates channel_1 and users3 creates channel_2
    user 2 join channel_1
    '''
    clear()
    auth.auth_register('test1@test.com', 'password', 'name_first', 'name_last')
    auth.auth_register('test2@test.com', 'password', 'name_first', 'name_last')
    auth.auth_register('test3@test.com', 'password', 'name_first', 'name_last')
    auth.auth_login('test1@test.com', 'password')
    auth.auth_login('test2@test.com', 'password')
    auth.auth_login('test3@test.com', 'password')
    channels_create(users[0]['token'], 'channel_1', True)
    channel_join(users[1]['token'], channels[0]['channel_id'])
    channels_create(users[2]['token'], 'channel_2', True)

@pytest.fixture
def initial_msgs():
    '''
    it is a fixture for tests.
    user 1 send 'msg_1' to channel_1 with msg_id 10001
    user 2 send 'msg_2' to channel_1 with msg_id 10002
    user 3 send 'msg_3' to channel_1 with msg_id 20001
    '''
    message_send(users[0]['token'], channels[0]['channel_id'], 'msg_1')
    message_send(users[1]['token'], channels[0]['channel_id'], 'msg_2')
    message_send(users[2]['token'], channels[1]['channel_id'], 'msg_3')

def test_msg_send(initial_data):
    '''test for message_send'''
    # 1. msg_send works well
    message_send(users[0]['token'], channels[0]['channel_id'], 'msg_1')
    message_send(users[1]['token'], channels[0]['channel_id'], 'a' * 1000)
    message_send(users[2]['token'], channels[1]['channel_id'], '')

    all_messages = channels[0]['messages']
    assert len(all_messages) == 2
    assert all_messages[0]['u_id'] == users[0]['u_id']
    assert all_messages[0]['message'] == 'msg_1'
    assert all_messages[0]['message_id'] == 10001
    assert all_messages[1]['u_id'] == users[1]['u_id']
    assert all_messages[1]['message'] == 'a' * 1000
    assert all_messages[1]['message_id'] == 10002

    all_messages = channels[1]['messages']
    assert len(all_messages) == 1
    assert all_messages[0]['u_id'] == users[2]['u_id']
    assert all_messages[0]['message'] == ''
    assert all_messages[0]['message_id'] == 20001

    # 2. input error when message is more than 1000 characters
    with pytest.raises(InputError):
        message_send(users[0]['token'], channels[0]['channel_id'], 'a' * 1001)

    # 3. access error 1 when given token does not refer to a valid user
    with pytest.raises(AccessError):
        message_send('invalid_token', channels[0]['channel_id'], 'msg')

    # 4. access error 2 when the authorised user has not joined the channel
    #    they are trying to post to or non-exsiting channel
    with pytest.raises(AccessError):
        message_send(users[0]['token'], channels[1]['channel_id'], 'msg')
    with pytest.raises(AccessError):
        message_send(users[1]['token'], channels[1]['channel_id'], 'msg')
    with pytest.raises(AccessError):
        message_send(users[2]['token'], channels[0]['channel_id'], 'msg')
    with pytest.raises(AccessError):
        message_send(users[2]['token'], 0, 'msg')

def test_msg_remove(initial_data, initial_msgs):
    ''' test for msg_remove'''
    # 1. msg_remove works well
    message_remove(users[1]['token'], 10002)    # removed by sender
    message_send(users[0]['token'], channels[0]['channel_id'], 'msg_4')
    all_messages = channels[0]['messages']
    assert len(all_messages) == 2
    assert all_messages[0]['u_id'] == users[0]['u_id']
    assert all_messages[0]['message'] == 'msg_1'
    assert all_messages[0]['message_id'] == 10001
    assert all_messages[1]['u_id'] == users[0]['u_id']
    assert all_messages[1]['message'] == 'msg_4'
    assert all_messages[1]['message_id'] == 10003

    message_remove(users[2]['token'], 20001) # removed by owner
    message_send(users[2]['token'], channels[1]['channel_id'], 'msg_5')
    message_send(users[2]['token'], channels[1]['channel_id'], 'msg_6')
    all_messages = channels[1]['messages']
    assert len(all_messages) == 2
    assert all_messages[0]['u_id'] == users[2]['u_id']
    assert all_messages[0]['message'] == 'msg_5'
    assert all_messages[0]['message_id'] == 20002
    assert all_messages[1]['u_id'] == users[2]['u_id']
    assert all_messages[1]['message'] == 'msg_6'
    assert all_messages[1]['message_id'] == 20003

    # 2. input error when message (based on ID) no longer exists
    with pytest.raises(InputError):
        message_remove(users[1]['token'], 10002)
    with pytest.raises(InputError):
        message_remove(users[1]['token'], 100002)

    # 3. access error 1 when given token does not refer to a valid user
    with pytest.raises(AccessError):
        message_remove('invalid_token', 10003)

    # 4. access error 2 when Message with message_id was sent by
    #   the authorised user making this request
    #   or The authorised user is an owner of this channel or the flockr
    with pytest.raises(AccessError):
        message_remove(users[1]['token'], 10003)

def test_msg_edit(initial_data, initial_msgs):
    '''test for msg_edit'''
    # 1. msg_edit works well
    message_edit(users[0]['token'], 10001, 'msg_new')
    message_edit(users[1]['token'], 10002, '')
    all_messages = channels[0]['messages']
    assert len(all_messages) == 1
    assert all_messages[0]['u_id'] == users[0]['u_id']
    assert all_messages[0]['message'] == 'msg_new'
    assert all_messages[0]['message_id'] == 10001

    message_edit(users[2]['token'], 20001, 'msg_new_2')
    all_messages = channels[1]['messages']
    assert len(all_messages) == 1
    assert all_messages[0]['u_id'] == users[2]['u_id']
    assert all_messages[0]['message'] == 'msg_new_2'
    assert all_messages[0]['message_id'] == 20001

    # 2. access error when given token does not refer to a valid user
    with pytest.raises(AccessError):
        message_edit('invalid_token', 20001, 'msg')

    # 3. access error when Message with message_id was sent by
    #   the authorised user making this request
    #   or The authorised user is an owner of this channel or the flockr
    with pytest.raises(AccessError):
        message_edit(users[1]['token'], 10001, 'msg')
    clear()
        
def test_msg_send_later(initial_data, initial_msgs):
    '''test for message_send_later'''
    
    # 1. Basic message success
    message_send_later(users[1]['token'], channels[0]['channel_id'], 'msg', time.time()+10)
    all_messages = channels[0]['messages']
    assert all_messages[0]['message_id'] == 10001
    
    # 2. InputError when message more than 1000 characters
    with pytest.raises(InputError):
        message_send_later(users[1]['token'], channels[0]['channel_id'], 'a' * 1001, time.time()+10)
    
    # 3. InputError when Channel ID is not a a valid channel 
    with pytest.raises(InputError):
        message_send_later(users[1]['token'], 0, 'msg', time.time()+10)
        
    # 4. InputError when time is in past
    with pytest.raises(InputError):
        message_send_later(users[1]['token'], channels[0]['channel_id'], 'msg', time.time()-10)
    
    # 5. AccessError when user hasn't joined channel
    with pytest.raises(AccessError):
        message_send_later(users[1]['token'], channels[1]['channel_id'], 'msg', time.time()+10)
        
def test_msg_react_unreact(initial_data, initial_msgs):
    '''test for message react and message unreact functions'''
    
    all_messages = channels[0]['messages']
    # 1. Basic react/unreact
    message_react(users[1]['token'], 10002, 1)
    assert all_messages[1]['reactors'] == [users[1]['u_id']]
    
    message_unreact(users[1]['token'], 10002, 1)
    assert all_messages[1]['reactors'] == []
    
    # 2. Not a valid message
    
    with pytest.raises(InputError):
        message_react(users[1]['token'], 10004, 1)
        
    with pytest.raises(InputError):
        message_unreact(users[1]['token'], 10004, 1)
    
    # 3. React id invalid
    
    with pytest.raises(InputError):
        message_react(users[1]['token'], 10002, 0)
    
    with pytest.raises(InputError):
        message_unreact(users[1]['token'], 10002, 0)
        
    # 4. Message already reacted/unreacted by user 
    
    message_react(users[1]['token'], 10002, 1)
    with pytest.raises(InputError):
        message_react(users[1]['token'], 10002, 1)
    
    message_unreact(users[1]['token'], 10002, 1)
    with pytest.raises(InputError):
        message_unreact(users[1]['token'], 10002, 1)
        
def test_msg_pin_unpin(initial_data, initial_msgs):
    
    # 1. Basic pin/unpin
    message_pin(users[0], 10001)
    assert all_messages[0]['pinned'] == True
    
    message_unpin(users[0], 10001)
    assert all_messages[0]['pinned'] == False
    
    # 2. message_id is invalid  
    
    with pytest.raises(InputError):
        message_pin(users[0], 10005)
    
    with pytest.raises(InputError):
        message_unpin(users[0], 10005)
        
    # 2. message_id is already pinned/unpinned
    message_pin(users[0], 10001)
    with pytest.raises(InputError):
        message_pin(users[0], 10001)
    
    message_unpin(users[0], 10001)
    with pytest.raises(InputError):
        message_unpin(users[0], 10001)
        
    # 3. user is not a member of the channel
    
    with pytest.raises(AccessError):
        message_pin(users[2], 10001)
        
    message_pin(users[0], 10001)
    with pytest.raises(AccessError):
        message_unpin(users[2], 10001)
        
    # 4. user is not an owner
    
    with pytest.raises(AccessError):
        message_unpin(users[1], 10001)
        
    message_unpin(users[0], 10001)
    with pytest.raises(AccessError):
        message_pin(users[1], 10001)
