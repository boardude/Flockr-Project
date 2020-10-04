# Yicheng (Mike) Zhu
# Last updated 4/10/2020

from channels import channels_list, channels_listall, channels_create, get_uid_from_token
from data import users, channels
from other import clear
from error import InputError
import pytest
import auth

"""
TESTS
        list:
            1. Prelim test: whether a dict is returned
            2. Standard functionality test according to spec
        listall:
            1. Prelim test: whether a dict is returned
            2. Standard functionality test according to spec
        create:
            1. Prelim test: Invalid name (longer than 20 characters)
            2. Prelim test: whether a dictionary is returned
            3. Standard test: correct ID returned + correct channel details registered
            4. Edge test: Duplicate details

HELPER FUNCTIONS
    1. register_and_login(email, password, first_name, last_name):
       registers and logs in user with provided details, returning the token
    2. create_channels(token_1, token_2): creates 6 test channels with tokens from two users
"""

##### GLOBAL VARIABLES #####
channel_01 = None
channel_02 = None
channel_03 = None
channel_04 = None
channel_05 = None
channel_06 = None

##### TEST IMPLEMENTATIONS #####
# Test that a dict containing an list of dictionaries, i.e. { channels }, 
# is the output
def test_list_return_type():
    clear()
    # register & log in user
    token = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')

    # test whether a dict is returned
    temp = channels_list(token)
    assert isinstance(temp, dict) is True

    # test whether a list is embedded within the dictionary appropriately
    assert isinstance(temp['channels'], list) is True
    for x in range(len(temp['channels'])):
        assert isinstance(temp['channels'][x], dict) is True

# Test for standard functionality of channels_list() according to spec
def test_list_standard():
    clear()
    # register & log in first user
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')

    # register & log in second user
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')

    # create test channels
    create_channels(token_1, token_2)

    # test length of returned channels list, making sure channels of 
    # User 2 is not listed
    temp = channels_list(token_1)
    assert len(temp['channels']) == 3

    # test for accuracy of details of returned channels list
    channel_01_listed = temp['channels'][0]
    channel_02_listed = temp['channels'][1]
    channel_03_listed = temp['channels'][2]
    assert channel_01_listed['channel_id'] == channel_01['channel_id']
    assert channel_01_listed['name'] == 'Channel 01'
    assert channel_02_listed['channel_id'] == channel_02['channel_id']
    assert channel_02_listed['name'] == 'Channel 02'
    assert channel_03_listed['channel_id'] == channel_03['channel_id']
    assert channel_03_listed['name'] == 'Channel 03'

# Test that a dict containing an list of dictionaries, i.e. { channels }, 
# is the output
def test_listall_return_type():
    clear()
    # register & log in user
    token = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')

    # test whether a dict is returned
    temp = channels_listall(token)
    assert isinstance(temp, dict) is True

    # test whether a list of dictionaries is embedded within the output appropriately
    assert isinstance(temp['channels'], list) is True
    for x in range(len(temp['channels'])):
        assert isinstance(temp['channels'][x], dict) is True

# Test for standard functionality of channels_listall() according to spec
def test_listall_standard():
    clear()
    # register & log in first user
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')

    # register & log in second user
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')

    # create test channels
    create_channels(token_1, token_2)

    # test length of returned channels list, making sure both 
    # users' channels are listed
    temp = channels_listall(token_1)
    assert len(temp['channels']) == 6

    # test for accuracy of details of returned channels list
    channel_01_listed = temp['channels'][0]
    channel_02_listed = temp['channels'][1]
    channel_03_listed = temp['channels'][2]
    channel_04_listed = temp['channels'][3]
    channel_05_listed = temp['channels'][4]
    channel_06_listed = temp['channels'][5]
    assert channel_01_listed['channel_id'] == channel_01['channel_id']
    assert channel_01_listed['name'] == 'Channel 01'
    assert channel_02_listed['channel_id'] == channel_02['channel_id']
    assert channel_02_listed['name'] == 'Channel 02'
    assert channel_03_listed['channel_id'] == channel_03['channel_id']
    assert channel_03_listed['name'] == 'Channel 03'
    assert channel_04_listed['channel_id'] == channel_04['channel_id']
    assert channel_04_listed['name'] == 'Channel 04 User 2'
    assert channel_05_listed['channel_id'] == channel_05['channel_id']
    assert channel_05_listed['name'] == 'Channel 05 User 2'
    assert channel_06_listed['channel_id'] == channel_06['channel_id']
    assert channel_06_listed['name'] == 'Channel 06 User 2'

# Test that a dict containing an int for channel_id, i.e. { channel_id }, 
# is the output
def test_create_return_type():
    clear()
    # register & log in user
    token = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')

    # test whether a dict is returned
    temp = channels_create(token, 'Channel 01', True)
    assert isinstance(temp, dict) is True

    # test whether an int is embedded appropriately within the returned dict
    assert isinstance(temp['channel_id'], int) is True

# InputError by channels_create() when name is longer than 20 characters
def test_create_invalid():
    clear()
    token = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')
    with pytest.raises(InputError) as e:
        channels_create(token, 'Channel NameThatHasMoreThanTwentyCharacters', True) # long character name exception 

# Test for standard functionality of channels_create() according to spec
def test_create_standard():
    clear()
    # register & log in first user
    token_1 = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')

    # register & log in second user
    token_2 = register_and_login('validuser2email@gmail.com', 'validpass2', 'User', 'Two')
    
    # create test channels
    create_channels(token_1, token_2)
    
    # test for accuracy of details in channels
    assert len(channels) == 6
    assert channels[0]['channel_id'] == channel_01['channel_id']
    assert channels[0]['name'] == 'Channel 01'
    assert channels[0]['public'] == True
    assert channels[1]['channel_id'] == channel_02['channel_id']
    assert channels[1]['name'] == 'Channel 02'
    assert channels[1]['public'] == False
    assert channels[2]['channel_id'] == channel_03['channel_id']
    assert channels[2]['name'] == 'Channel 03'
    assert channels[2]['public'] == True
    assert channels[3]['channel_id'] == channel_04['channel_id']
    assert channels[3]['name'] == 'Channel 04 User 2'
    assert channels[3]['public'] == True
    assert channels[4]['channel_id'] == channel_05['channel_id']
    assert channels[4]['name'] == 'Channel 05 User 2'
    assert channels[4]['public'] == False
    assert channels[5]['channel_id'] == channel_06['channel_id']
    assert channels[5]['name'] == 'Channel 06 User 2'
    assert channels[5]['public'] == False

    # test for accuracy of details in users' channels list
    user_1_channels = users[0]['channels']
    user_2_channels = users[1]['channels']
    assert len(user_1_channels) == 3
    assert len(user_2_channels) == 3
    assert user_1_channels[0] == channel_01['channel_id']
    assert user_1_channels[1] == channel_02['channel_id']
    assert user_1_channels[2] == channel_03['channel_id']
    assert user_2_channels[0] == channel_04['channel_id']
    assert user_2_channels[1] == channel_05['channel_id']
    assert user_2_channels[2] == channel_06['channel_id']

    # check for channel ownership of first user
    uid_1 = get_uid_from_token(token_1)
    is_owner = False
    for x in range(0, 3):
        for owner in channels[x]['owner_members']:
            if owner == uid_1:
                is_owner = True
    assert is_owner is True

    # check for channel ownership of second user
    uid_2 = get_uid_from_token(token_2)
    is_owner = False
    for x in range(3, 6):
        for owner in channels[x]['owner_members']:
            if owner == uid_2:
                is_owner = True
    assert is_owner is True

# When two channels with duplicate details are created
# Ensure both are created as they differ by channel_id
def test_create_duplicate():
    clear()
    # register & log in user
    token = register_and_login('validuseremail@gmail.com', 'validpass', 'User', 'One')

    # create test channels
    global channel_01, channel_02
    channel_01 = channels_create(token, 'Channel Same Name', True)
    channel_02 = channels_create(token, 'Channel Same Name', True)

    # test for accuracy of details in channels
    assert len(channels) == 2
    assert channels[0]['channel_id'] == channel_01['channel_id']
    assert channels[0]['name'] == 'Channel Same Name'
    assert channels[0]['public'] == True
    assert channels[1]['channel_id'] == channel_02['channel_id']
    assert channels[1]['name'] == 'Channel Same Name'
    assert channels[1]['public'] == True

    # check for channel ownership
    uid = get_uid_from_token(token)
    is_owner = False
    for channel in channels:
        for owner in channel['owner_members']:
            if owner == uid:
                is_owner = True
    assert is_owner is True

    # ensure the two "duplicate" channels differ by channel_id
    assert channel_01['channel_id'] != channel_02['channel_id']


##### HELPER FUNCTIONS #####
# registers and logs in user with provided details, returning the token
def register_and_login(email, password, first_name, last_name):
    auth.auth_register(email, password, first_name, last_name)
    login = auth.auth_login(email, password)
    return login['token']

# creates 6 test channels with tokens from two users
def create_channels(token_1, token_2):
    global channel_01, channel_02, channel_03, channel_04, channel_05, channel_06

    channel_01 = channels_create(token_1, 'Channel 01', True)
    channel_02 = channels_create(token_1, 'Channel 02', False)
    channel_03 = channels_create(token_1, 'Channel 03', True)
    channel_04 = channels_create(token_2, 'Channel 04 User 2', True)
    channel_05 = channels_create(token_2, 'Channel 05 User 2', False)
    channel_06 = channels_create(token_2, 'Channel 06 User 2', False) 
