import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import pytest
from auth import token_generate

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

@pytest.fixture
def create_users(url):
    # clear data
    requests.delete(url + 'clear')

    # register & log in 2 users
    for i in range(2):
        user_data = {
            'password' : 'validpass' + str(i+1),
            'name_first': 'User',
            'name_last' : '0' + str(i+1),
            'email': 'validuser' + str(i+1) + 'email@gmail.com',
        }
        requests.post(url + 'auth/register', json=user_data)
        resp = requests.post(url + 'auth/login', json=user_data)

@pytest.fixture
def create_channels(url):
    """
        Creates 6 test channels with tokens from two users
        returned channel_id's are stored in global variables
    """
    channel_data = {
        'token': token_generate(1, 'login'),
        'channel_name': 'Channel 01',
        'is_public': True,
    }
    requests.post(url + 'channels/create', json=channel_data)

    channel_data = {
        'token': token_generate(1, 'login'),
        'channel_name': 'Channel 02',
        'is_public': False,
    }
    requests.post(url + 'channels/create', json=channel_data)

    channel_data = {
        'token': token_generate(1, 'login'),
        'channel_name': 'Channel 03',
        'is_public': True,
    }
    requests.post(url + 'channels/create', json=channel_data)

    channel_data = {
        'token': token_generate(1, 'login'),
        'channel_name': 'Channel 03',
        'is_public': True,
    }
    requests.post(url + 'channels/create', json=channel_data)

    channel_data = {
        'token': token_generate(2, 'login'),
        'channel_name': 'Channel 04 User 02',
        'is_public': True,
    }
    requests.post(url + 'channels/create', json=channel_data)

    channel_data = {
        'token': token_generate(2, 'login'),
        'channel_name': 'Channel 05 User 02',
        'is_public': False,
    }
    requests.post(url + 'channels/create', json=channel_data)

    channel_data = {
        'token': token_generate(2, 'login'),
        'channel_name': 'Channel 06 User 02',
        'is_public': False,
    }
    requests.post(url + 'channels/create', json=channel_data)

def test_http_list_invalid_token(url, create_users, create_channels):
    """
        Test for AccessError exception thrown by channels_create() when token
        passed in is not a valid token
    """
    # empty
    r = requests.get(url + 'channels/list', params={'token': ''})
    assert r.status_code == 400

    # None
    r = requests.get(url + 'channels/list', params={'token': None})
    assert r.status_code == 400

    # Not the correct data type
    r = requests.get(url + 'channels/list', params={'token': 123})
    assert r.status_code == 400

    # Not an authorised user
    bad_token = 'invalid_token'
    r = requests.get(url + 'channels/list', params={'token': bad_token})
    assert r.status_code == 400

def test_http_list_standard(url, create_users, create_channels):
    """
        Test for standard functionality of channels_list() according to spec
    """
    r = requests.get(url + 'channels/list', params={'token': token_generate(1, 'login')})
    payload = r.json()

    # test length and accuracy of returned channels list, making sure 
    # channels of User 2 is not listed
    assert len(payload['channels']) == 3
    channel_01_listed = payload['channels'][0]
    channel_02_listed = payload['channels'][1]
    channel_03_listed = payload['channels'][2]
    assert channel_01_listed['channel_id'] == channel_01['channel_id']
    assert channel_01_listed['name'] == 'Channel 01'
    assert channel_02_listed['channel_id'] == channel_02['channel_id']
    assert channel_02_listed['name'] == 'Channel 02'
    assert channel_03_listed['channel_id'] == channel_03['channel_id']
    assert channel_03_listed['name'] == 'Channel 03'

def test_http_listall_invalid_token(url, create_users, create_channels):
    """
        Test for AccessError exception thrown by channels_create() when token
        passed in is not a valid token
    """
    # empty
    r = requests.get(url + 'channels/listall', params={'token': ''})
    assert r.status_code == 400

    # None
    r = requests.get(url + 'channels/listall', params={'token': None})
    assert r.status_code == 400

    # Not the correct data type
    r = requests.get(url + 'channels/listall', params={'token': 123})
    assert r.status_code == 400

    # Not an authorised user
    bad_token = 'invalid_token'
    r = requests.get(url + 'channels/listall', params={'token': bad_token})
    assert r.status_code == 400

def test_http_listall_standard(url, create_users, create_channels):
    """
        Test for standard functionality of channels_list() according to spec
    """
    r = requests.get(url + 'channels/listall', params={'token': token_generate(1, 'login')})
    payload = r.json()

    # test length and accuracy of returned channels list, making sure 
    # channels of User 2 is not listed
    assert len(payload['channels']) == 6
    channel_01_listed = payload['channels'][0]
    channel_02_listed = payload['channels'][1]
    channel_03_listed = payload['channels'][2]
    channel_04_listed = payload['channels'][3]
    channel_05_listed = payload['channels'][4]
    channel_06_listed = payload['channels'][5]
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

def test_http_create_invalid_name(url, create_users):
    """
        Test for InputError exception thrown by channels_create() when name
        is longer than 20 characters
    """
    query = {
        'token': token_generate(1, 'login'),
        'channel_name': 'Channel NameThatHasMoreThanTwentyCharacters',
        'is_public': True,
    }
    r = requests.post(url + 'channels/create', json=query)
    assert r.status_code == 400

def test_http_create_standard(url, create_users):
    """
        Test for standard functionality of channels_create() according to spec
    """
    query = {
        'token': token_generate(1, 'login'),
        'channel_name': 'Channel 01',
        'is_public': True,
    }
    r = requests.post(url + 'channels/create', json=query)
    assert r.status_code == 200

def test_http_create_duplicate(url, create_users):
    """
        When two channels with duplicate details are created
        Ensure both are created as they differ by channel_id
    """    
    query = {
        'token': token_generate(1, 'login'),
        'channel_name': 'Channel 01',
        'is_public': True,
    }
    r = requests.post(url + 'channels/create', json=query)
    assert r.status_code == 200

    r = requests.post(url + 'channels/create', json=query)
    assert r.status_code == 200
