from channels import channels_list, channels_listall, channels_create
from other import clear
from error import InputError
import pytest
import auth.py

''' Tests:
        list:
            1. Prelim test: whether a list is returned
            2. Standard test: correct list returned
        listall:
            1. Prelim test: whether a list is returned
            2. Standard test: correct list returned
        create:
            1. Prelim test: Invalid name (longer than 20 characters)
            2. Prelim test: whether a dictionary is returned
            3. Standard test: correct ID returned + correct channel details registered
'''

def test_list_return_type():
    clear()
    temp = channels_list('validusertoken')
    assert isinstance(temp, list) is True

def test_list_standard():
    clear()
    # register & log in first user
    auth.auth_register('validuseremail@gmail.com', 'validpass', 'User', 'One')
    login = auth.auth_login('validuseremail@gmail.com', 'validpass')
    token = login['token']

    # create channels
    channel_00 = channels_create(token, 'Channel 00', True)
    channel_01 = channels_create(token, 'Channel 01', False)
    channel_02 = channels_create(token, 'Channel 02', True)

    # test channels_list
    temp = channels_list('validusertoken')
    assert len(temp) == 3
    assert temp[0]['channel_id'] == channel_00['channel_id']
    assert temp[0]['name'] == 'Channel 00'
    assert temp[0]['public'] == True
    assert temp[1]['channel_id'] == channel_01['channel_id']
    assert temp[1]['name'] == 'Channel 01'
    assert temp[1]['public'] == False
    assert temp[2]['channel_id'] == channel_02['channel_id']
    assert temp[2]['name'] == 'Channel 02'
    assert temp[2]['public'] == True

def test_listall_return_type():
    clear()
    temp = channels_listall('validusertoken')
    assert isinstance(temp, list) is True

def test_listall_standard():
    clear()
    # register & log in first user
    auth.auth_register('validuseremail@gmail.com', 'validpass', 'User', 'One')
    login = auth.auth_login('validuseremail@gmail.com', 'validpass')
    token = login['token']

    # register & log in second user
    auth.auth_register('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    login_2 = auth.auth_login('validuser2email@gmail.com', 'validpass2')
    token_2 = login_2['token']

    # create channels
    channel_00 = channels_create(token, 'Channel 00', True)
    channel_01 = channels_create(token, 'Channel 01', False)
    channel_02 = channels_create(token, 'Channel 02', True)
    channel_03 = channels_create(token_2, 'Channel 03 User 2', True)
    channel_04 = channels_create(token_2, 'Channel 04 User 2', False)
    channel_05 = channels_create(token_2, 'Channel 05 user 2', False)

    # test channels_listall
    temp = channels_listall('validusertoken')
    assert len(temp) == 6
    assert temp[0]['channel_id'] == channel_00['channel_id']
    assert temp[0]['name'] == 'Channel 00'
    assert temp[0]['public'] == True
    assert temp[1]['channel_id'] == channel_01['channel_id']
    assert temp[1]['name'] == 'Channel 01'
    assert temp[1]['public'] == False
    assert temp[2]['channel_id'] == channel_02['channel_id']
    assert temp[2]['name'] == 'Channel 02'
    assert temp[2]['public'] == True
    assert temp[3]['channel_id'] == channel_03['channel_id']
    assert temp[3]['name'] == 'Channel 03 User 2'
    assert temp[3]['public'] == True
    assert temp[4]['channel_id'] == channel_04['channel_id']
    assert temp[4]['name'] == 'Channel 04 User 2'
    assert temp[4]['public'] == False
    assert temp[5]['channel_id'] == channel_05['channel_id']
    assert temp[5]['name'] == 'Channel 05 User 2'
    assert temp[5]['public'] == False


def test_create_return_type():
    clear()
    temp = channels_create('validusertoken', 'Channel 01', True)
    assert isinstance(temp, dict) is True

def test_create_invalid_name():

    clear()
    with pytest.raises(InputError) as e:  # InputError test
        channels_create('longnameusertoken', 'Channel NameThatHasMoreThanTwentyCharacters', True) # long character name exception 

    clear()
    with pytest.raises(InputError) as e:  # InputError test no token
        channels_create('', 'Channel NameThatHasMoreThanTwentyCharacters', True)

def test_create_standard():
    clear()
    # register & log in first user
    auth.auth_register('validuseremail@gmail.com', 'validpass', 'User', 'One')
    login = auth.auth_login('validuseremail@gmail.com', 'validpass')
    token = login['token']

    # create channels
    channel_00 = channels_create(token, 'Channel Zero', True)
    channel_01 = channels_create(token, 'Channel One', True)
    channel_02 = channels_create(token， 'Channel Two', False)
    
    # test if channels have been created with correct details
    temp = channels_list(token)
    assert len(temp) == 3
    assert temp[0]['channel_id'] == channel_00['channel_id']
    assert temp[0]['name'] == 'Channel Zero'
    assert temp[0]['public'] == True
    assert temp[1]['channel_id'] == channel_01['channel_id']
    assert temp[1]['name'] == 'Channel One'
    assert temp[1]['public'] == True
    assert temp[2]['channel_id'] == channel_02['channel_id']
    assert temp[2]['name'] == 'Channel Two'
    assert temp[2]['public'] == False