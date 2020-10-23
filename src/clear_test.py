# Yicheng (Mike) Zhu
# Last updated 22/10/2020

from other import clear
from data import users, channels
from channels import channels_create
from auth import auth_login, auth_register

def test_clear_standard():
    # initial clear
    clear()

    # preliminary assertions
    assert len(users) == 0
    assert len(channels) == 0

    # create users
    auth_register('validuseremail@gmail.com', 'validpass', 'User', 'One')
    auth_register('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    token_1 = auth_login('validuseremail@gmail.com', 'validpass')['token']
    token_2 = auth_login('validuser2email@gmail.com', 'validpass2')['token']

    # create channels
    channels_create(token_1, 'Channel 01', True)
    channels_create(token_1, 'Channel 02', False)
    channels_create(token_2, 'Channel 03', False)

    # intermediate assertions
    assert len(users) == 2
    assert len(channels) == 3

    # invoke clear() for testing
    clear()

    # final assertions
    assert len(users) == 0
    assert len(channels) == 0
