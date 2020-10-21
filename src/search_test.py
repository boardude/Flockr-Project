import pytest
from other import search, clear
from helper import register_and_login, get_random_str, get_uid_from_token
from data import users
from error import AccessError
from channels import channels_create
from message import message_send

def test_search_invalid_token():
    clear()
    # register two users
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')

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
    bad_token = get_random_str(6)
    while bad_token is token_1 or bad_token is token_2:
        bad_token = get_random_str(6)

    with pytest.raises(AccessError):
        search(bad_token, 'query')

def test_search_standard():
    clear()
    # register two users
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    uid_1 = get_uid_from_token(token_1)
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    uid_2 = get_uid_from_token(token_2)

    # create channels for the first user
    user01_channel01 = channels_create(token_1, 'Channel 01 User 01', True)
    user01_channel02 = channels_create(token_1, 'Channel 02 User 01', False)

    # create channels for the second user
    user02_channel01 = channels_create(token_2, 'Channel 01 User 02', False)
    user02_channel02 = channels_create(token_2, 'Channel 02 User 02', True)

    # send messages for first user
    msg11 = message_send(token_1, user01_channel01['channel_id'], 'Hello, channel one')
    msg12 = message_send(token_1, user01_channel02['channel_id'], 'Hello, channel two?')
    msg13 = message_send(token_1, user01_channel01['channel_id'], 'Wait is this really channel one?')
    msg14 = message_send(token_1, user01_channel01['channel_id'], 'Yep it is!')
    msg15 = message_send(token_1, user01_channel02['channel_id'], 'Hola amigos!')

    # send messages for the second user
    msg21 = message_send(token_2, user02_channel01['channel_id'], 'What\'s up channel one')
    msg22 = message_send(token_2, user02_channel02['channel_id'], 'What\'s up channel two')
    msg23 = message_send(token_2, user02_channel01['channel_id'], 'You channel one or What?')
    msg24 = message_send(token_2, user02_channel01['channel_id'], 'What? Yeah bro I am')
    msg25 = message_send(token_2, user02_channel02['channel_id'], 'What?')

    # invoke and test search()
    messages = search(token_1, 'Hello')
    assert len(messages['messages']) == 2
    assert messages['messages'][0]['message_id'] == msg12['message_id']
    assert messages['messages'][0]['u_id'] == uid_1
    assert messages['messages'][0]['message'] == 'Hello, channel two?'
    assert messages['messages'][1]['message_id'] == msg11['message_id']
    assert messages['messages'][1]['u_id'] == uid_1
    assert messages['messages'][1]['message'] == 'Hello, channel one'

    messages = search(token_1, 'Hola')
    assert len(messages['messages']) == 1
    assert messages['messages'][0]['message_id'] == msg15['message_id']
    assert messages['messages'][0]['u_id'] == uid_1
    assert messages['messages'][0]['message'] == 'Hola amigos!'

    messages = search(token_1, '?')
    assert len(messages['messages']) == 2
    assert messages['messages'][0]['message_id'] == msg12['message_id']
    assert messages['messages'][0]['u_id'] == uid_1
    assert messages['messages'][0]['message'] == 'Hello, channel two?'
    assert messages['messages'][1]['message_id'] == msg13['message_id']
    assert messages['messages'][1]['u_id'] == uid_1
    assert messages['messages'][1]['message'] == 'Wait is this really channel one?'


    messages = search(token_2, 'What')
    assert len(messages['messages']) == 5
    assert messages['messages'][0]['message_id'] == msg21['message_id']
    assert messages['messages'][0]['u_id'] == uid_2
    assert messages['messages'][0]['message'] == 'What\'s up channel one'
    assert messages['messages'][1]['message_id'] == msg23['message_id']
    assert messages['messages'][1]['u_id'] == uid_2
    assert messages['messages'][1]['message'] == 'You channel one or What?'
    assert messages['messages'][2]['message_id'] == msg24['message_id']
    assert messages['messages'][2]['u_id'] == uid_2
    assert messages['messages'][2]['message'] == 'What? Yeah bro I am'
    assert messages['messages'][3]['message_id'] == msg22['message_id']
    assert messages['messages'][3]['u_id'] == uid_2
    assert messages['messages'][3]['message'] == 'What\'s up channel two'
    assert messages['messages'][4]['message_id'] == msg25['message_id']
    assert messages['messages'][4]['u_id'] == uid_2
    assert messages['messages'][4]['message'] == 'What?'

