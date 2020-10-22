# Yicheng (Mike) Zhu
# Last updated 22/10/2020

from other import clear
from data import users, channels
from channels import channels_create
from helper import register_and_login

def test_clear_standard():
    # initial clear
    clear()

    # preliminary assertions
    assert len(users) == 0
    assert len(channels) == 0

    # create users
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')

    # create channels
    channel_01 = channels_create(token_1, 'Channel 01', True)
    channel_02 = channels_create(token_1, 'Channel 02', False)
    channel_03 = channels_create(token_2, 'Channel 03', False)

    # intermediate assertions
    assert len(users) == 2
    assert len(channels) == 3

    # invoke clear() for testing
    clear()

    # final assertions
    assert len(users) == 0
    assert len(channels) == 0
