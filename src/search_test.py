import pytest
from other import search, register_and_login, clear, get_random_str, get_uid_from_token
from data import users
from error import AccessError
from channels import channels_create
from messages import message_send

def test_search_invalid_token():
    clear()
    # register two users
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')

    # empty
    with pytest.raises(AccessError):
        search('')

    # None
    with pytest.raises(AccessError):
        search(None)

    # Not the correct data type
    with pytest.raises(AccessError):
        search(123)

    # Not an authorised user
    bad_token = get_random_str(6)
    while bad_token is token_1 or bad_token is token_2:
        bad_token = get_random_str(6)

    with pytest.raises(AccessError):
        search(bad_token)

def test_search_standard():
    clear()
    # register two users
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')

    # create channels for the first user
    user01_channel01 = channels_create(token_1, 'Channel 01 User 01', True)
    user01_channel02 = channels_create(token_1, 'Channel 02 User 01', False)

    # create channels for the second user
    user02_channel01 = channels_create(token_2, 'Channel 01 User 02', False)
    user02_channel02 = channels_create(token_2, 'Channel 02 User 02', True)

    # send messages for 