import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import pytest

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
def initial_users(url):
    # this function would clear all data and create 3 users
    requests.delete(url + 'clear')
    input = {
        'password' : 'password',
        'name_first': 'u',
        'name_last' : '1',
        }
    for idx in range(3):
        input['email'] = str(idx + 1) + 'test@test.com'
        requests.post(url + 'auth/register', json=input)

def http_test_channel_valid_invite(url, initial_users):
    '''
        valid test
    '''
    ###login three users

    input = {
        'email' : '1test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    u1_id = json.loads(resp.text)['u_id']
    input = {
        'email' : '2test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    token2 = json.loads(resp.text)['token']

    input = {
        'email' : '3test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    u3_id = json.loads(resp.text)['u_id']

    ###user 2 create a channel
    input = {
        'token' : token2,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id = json.loads(resp.text)['channel_id']

    ###user2 invite user1
    input = {
        'token' : token2,
        'channel_id' : channel_id,
        'u_id' : u1_id
    }
    resp = requests.post(url + 'channel/invite', json=input)
    assert resp.status_code == 200

    ###user2 invite user3
    input = {
        'token' : token2,
        'channel_id' : channel_id,
        'u_id' : u3_id
    }
    resp = requests.post(url + 'channel/invite', json=input)
    assert resp.status_code == 200

def http_test_channel_invite_invalid_channel_id(url, initial_users):
    '''
        invalid test of worng channel id
    '''
    ### login user1 and get the return token

    input = {
        'email' : '1test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    token1 = json.loads(resp.text)['token']

    ### login user2 and get the return u_id
    input = {
        'email' : '2test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    u2_id = json.loads(resp.text)['u_id']

    ###user 1 create a channel
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id = json.loads(resp.text)['channel_id']

    ###user 1 invite user2
    input = {
        'token' : token1,
        'channel_id' : channel_id + 1,
        'u_id' : u2_id
    }
    resp = requests.post(url + 'channel/invite', json=input)
    assert resp.status_code == 400

def http_test_channel_invite_invalid_u_id(url, initial_users):
    '''
        invlaid http test of invalid u_id
    '''
    ###login three users

    input = {
        'email' : '1test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    token1 = json.loads(resp.text)['token']

    ###user 1 create a channel
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id = json.loads(resp.text)['channel_id']
    ###user 1 invite a user who is not exist
    input = {
        'token' : token1,
        'channel_id' : channel_id,
        'u_id' : 0
    }
    resp = requests.post(url + 'channel/invite', json=input)
    assert resp.status_code == 400
def http_test_channel_invite_not_authorised_member():
    '''
        invalid test of the authorised user is not already a member of the channel
        login 3 users
        user1 create a channel
        user 2 who is not the channel owner invites user3
    '''
    ###login three users

    input = {
        'email' : '1test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    token1 = json.loads(resp.text)['token']
    input = {
        'email' : '2test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    token2 = json.loads(resp.text)['token']

    input = {
        'email' : '3test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    u3_id = json.loads(resp.text)['u_id']

    ###user 1 create a channel
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id = json.loads(resp.text)['channel_id']
    ###user 1 invite a user who is not exist
    input = {
        'token' : token2,
        'channel_id' : channel_id,
        'u_id' : u3_id
    }
    resp = requests.post(url + 'channel/invite', json=input)
    assert resp.status_code == 400
    