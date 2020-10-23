# Yicheng (Mike) Zhu
# Last updated 21/10/2020

import pytest
from other import search, clear
from auth import auth_login, auth_register
from data import users
from error import AccessError
from channels import channels_create
from channel import channel_join
from message import message_send

@pytest.fixture
def create_users():
    clear()
    auth_register('validuseremail@gmail.com', 'validpass', 'User', 'One')
    auth_register('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    auth_register('validuser3email@gmail.com', 'validpass3', 'User', 'Three')
    auth_login('validuseremail@gmail.com', 'validpass')
    auth_login('validuser2email@gmail.com', 'validpass2')
    auth_login('validuser3email@gmail.com', 'validpass3')

def test_search_invalid_token(create_users):
    # empty
    with pytest.raises(AccessError):
        search('', 'query')

    # None
    with pytest.raises(AccessError):
        search(None, 'query')

    # Not the correct data type
    with pytest.raises(AccessError):
        search(123, 'query')

    # Not an authorised user
    bad_token = 'invalid_token'

    with pytest.raises(AccessError):
        search(bad_token, 'query')

def test_search_no_cross_join_channel(create_users):
    # create channels for the first user
    user01_channel01 = channels_create(users[0]['token'], 'Channel 01 User 01', True)
    user01_channel02 = channels_create(users[0]['token'], 'Channel 02 User 01', False)

    # create channels for the second user
    user02_channel01 = channels_create(users[1]['token'], 'Channel 01 User 02', False)
    user02_channel02 = channels_create(users[1]['token'], 'Channel 02 User 02', True)

    # send messages for first user
    msg11 = message_send(users[0]['token'], user01_channel01['channel_id'], 'Hello, channel one')
    msg12 = message_send(users[0]['token'], user01_channel02['channel_id'], 'Hello, channel two?')
    msg13 = message_send(users[0]['token'], user01_channel01['channel_id'], 'Wait is this really channel one?')
    msg14 = message_send(users[0]['token'], user01_channel01['channel_id'], 'Yep it is?')
    msg15 = message_send(users[0]['token'], user01_channel02['channel_id'], 'Hola amigos!')

    # send messages for the second user
    msg21 = message_send(users[1]['token'], user02_channel01['channel_id'], 'What\'s up channel one')
    msg22 = message_send(users[1]['token'], user02_channel02['channel_id'], 'What\'s up channel two')
    msg23 = message_send(users[1]['token'], user02_channel01['channel_id'], 'You channel one or What?')
    msg24 = message_send(users[1]['token'], user02_channel01['channel_id'], 'What? Yeah I am')
    msg25 = message_send(users[1]['token'], user02_channel02['channel_id'], 'What?')

    # invoke and test search()
    messages = search(users[0]['token'], 'Hello')
    assert len(messages['messages']) == 2
    assert messages['messages'][0]['message_id'] == msg11['message_id']
    assert messages['messages'][0]['u_id'] == users[0]['u_id']
    assert messages['messages'][0]['message'] == 'Hello, channel one'
    assert messages['messages'][1]['message_id'] == msg12['message_id']
    assert messages['messages'][1]['u_id'] == users[0]['u_id']
    assert messages['messages'][1]['message'] == 'Hello, channel two?'

    messages = search(users[0]['token'], 'Hola')
    assert len(messages['messages']) == 1
    assert messages['messages'][0]['message_id'] == msg15['message_id']
    assert messages['messages'][0]['u_id'] == users[0]['u_id']
    assert messages['messages'][0]['message'] == 'Hola amigos!'

    messages = search(users[0]['token'], '?')
    assert len(messages['messages']) == 3
    assert messages['messages'][0]['message_id'] == msg13['message_id']
    assert messages['messages'][0]['u_id'] == users[0]['u_id']
    assert messages['messages'][0]['message'] == 'Wait is this really channel one?'
    assert messages['messages'][1]['message_id'] == msg14['message_id']
    assert messages['messages'][1]['u_id'] == users[0]['u_id']
    assert messages['messages'][1]['message'] == 'Yep it is?'
    assert messages['messages'][2]['message_id'] == msg12['message_id']
    assert messages['messages'][2]['u_id'] == users[0]['u_id']
    assert messages['messages'][2]['message'] == 'Hello, channel two?'

    messages = search(users[1]['token'], 'What')
    assert len(messages['messages']) == 5
    assert messages['messages'][0]['message_id'] == msg21['message_id']
    assert messages['messages'][0]['u_id'] == users[1]['u_id']
    assert messages['messages'][0]['message'] == 'What\'s up channel one'
    assert messages['messages'][1]['message_id'] == msg23['message_id']
    assert messages['messages'][1]['u_id'] == users[1]['u_id']
    assert messages['messages'][1]['message'] == 'You channel one or What?'
    assert messages['messages'][2]['message_id'] == msg24['message_id']
    assert messages['messages'][2]['u_id'] == users[1]['u_id']
    assert messages['messages'][2]['message'] == 'What? Yeah I am'
    assert messages['messages'][3]['message_id'] == msg22['message_id']
    assert messages['messages'][3]['u_id'] == users[1]['u_id']
    assert messages['messages'][3]['message'] == 'What\'s up channel two'
    assert messages['messages'][4]['message_id'] == msg25['message_id']
    assert messages['messages'][4]['u_id'] == users[1]['u_id']
    assert messages['messages'][4]['message'] == 'What?'

def test_search_cross_join_channel(create_users):
    # create a channel from user 1
    channel = channels_create(users[0]['token'], 'Channel 01 User 01', True)

    # user 2 joins user 1's channel
    channel_join(users[1]['token'], channel['channel_id'])

    # send messages from both users
    msg1 = message_send(users[0]['token'], channel['channel_id'], 'What\'s up user two')
    msg2 = message_send(users[1]['token'], channel['channel_id'], 'What\'s up user one')
    msg3 = message_send(users[1]['token'], channel['channel_id'], 'You user one or What?')
    msg4 = message_send(users[0]['token'], channel['channel_id'], 'What? Yeah I am')
    msg5 = message_send(users[1]['token'], channel['channel_id'], 'What?')

    # search from first user
    messages = search(users[0]['token'], 'What')

    # make sure messages from both users appear
    assert len(messages['messages']) == 5
    assert messages['messages'][0]['message_id'] == msg1['message_id']
    assert messages['messages'][0]['u_id'] == users[0]['u_id']
    assert messages['messages'][0]['message'] == 'What\'s up user two'
    assert messages['messages'][1]['message_id'] == msg2['message_id']
    assert messages['messages'][1]['u_id'] == users[1]['u_id']
    assert messages['messages'][1]['message'] == 'What\'s up user one'
    assert messages['messages'][2]['message_id'] == msg3['message_id']
    assert messages['messages'][2]['u_id'] == users[1]['u_id']
    assert messages['messages'][2]['message'] == 'You user one or What?'
    assert messages['messages'][3]['message_id'] == msg4['message_id']
    assert messages['messages'][3]['u_id'] == users[0]['u_id']
    assert messages['messages'][3]['message'] == 'What? Yeah I am'
    assert messages['messages'][4]['message_id'] == msg5['message_id']
    assert messages['messages'][4]['u_id'] == users[1]['u_id']
    assert messages['messages'][4]['message'] == 'What?'
