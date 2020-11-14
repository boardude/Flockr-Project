import pytest
import re
from subprocess import Popen, PIPE
import signal
import requests
import json
from auth import token_generate
from time import sleep

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
def initial_conditions(url):
    # creates 5 users, user 1 creates a channel, the rest write a message to
    # that channel user 1 and 2 are owners
    user_data = {
        'password' : 'password',
        'name_first': '1',
        'name_last' : '1',
        }
    for idx in range(5):
        email = str(idx + 1) + 'test@test.com'
        user_data['email'] = email
        requests.post(url + 'auth/register', json=user_data)
        resp = requests.post(url + 'auth/login', json={'email': email, 'password': 'password'})
        if idx == 0:
            token = json.loads(resp.text)['token']
            channel_data = {
                'token' : token,
                'name' : 'channel' + str(idx),
                'is_public' : True,
            }
            requests.post(url + 'channels/create', json=channel_data)
        else:
            requests.post(url + 'channel/join', json=
                    {'token': token_generate(idx + 1, 'login'), 'channel_id': 1})
            data = {
                'token' : token_generate(idx + 1, 'login'),
                'channel_id' : 1,
                'message' : 'message ' + str(idx),
            }
            requests.post(url + 'message/send', json = data)
            if idx == 1:
                data = {
                    'token' : token_generate(1, 'login'),
                    'channel_id' : 1,
                    'u_id' : 2,
                }
                requests.post(url + 'channel/addowner', json=data)


### MESSAGE SEND TESTS
def test_send_standard(url, initial_conditions):
    #standard send
    data = {
        'token' : token_generate(1, 'login'),
        'channel_id' : 1,
        'message' : 'This is the first message.',
    }
    resp = requests.post(url + 'message/send', json = data)
    assert resp.status_code == 200
    
def test_send_bad_message(url, initial_conditions):
    #message over 1000 characters
    data = {
        'token' : token_generate(1, 'login'),
        'channel_id' : 1,
        'message' : 'c' * 1001,
    }
    resp = requests.post(url + 'message/send', json = data)
    assert resp.status_code == 400

def test_send_bad_channel(url, initial_conditions):
    #incorrect channel_id
    data = {
        'token' : token_generate(1, 'login'),
        'channel_id' : 0,
        'message' : 'this shouldnt work',
    }
    resp = requests.post(url + 'message/send', json = data)
    assert resp.status_code == 400

def test_send_invalid_token(url, initial_conditions):
    #incorrect channel_id
    data = {
        'token' : token_generate(1, 'logout'),
        'channel_id' : 0,
        'message' : 'this shouldnt work',
    }
    resp = requests.post(url + 'message/send', json = data)
    assert resp.status_code == 400

### MESSAGE REMOVE TESTS
def test_remove_standard(url, initial_conditions):
    #standard remove
    data = {
        'token' : token_generate(1, 'login'),
        'message_id' : 10001,
    }
    msg_data = {
        'token' : token_generate(1, 'login'),
        'channel_id' : 1,
        'start' : 0,
    }
    # check all msgs
    resp = requests.get(url + 'channel/messages', params=msg_data)
    assert len(json.loads(resp.text)['messages']) == 4
    # do remove
    resp = requests.delete(url + 'message/remove', json = data)
    assert resp.status_code == 200
    # check all msgs
    resp = requests.get(url + 'channel/messages', params=msg_data)
    assert len(json.loads(resp.text)['messages']) == 3

def test_remove_message_id(url, initial_conditions):
    # message not sent by user
    data = {
        'token' : token_generate(5, 'login'),
        'message_id' : 10002,
    }
    resp = requests.delete(url + 'message/remove', json = data)
    assert resp.status_code == 400
    
    # message sent by user
    data = {
        'token' : token_generate(2, 'login'),
        'message_id' : 10002,
    }
    resp = requests.delete(url + 'message/remove', json = data)
    assert resp.status_code == 200

def test_remove_owner(url, initial_conditions):
    #user not owner of channel
    data = {
        'token' : token_generate(3, 'login'),
        'message_id' : 10003,
    }
    resp = requests.delete(url + 'message/remove', json = data)
    assert resp.status_code == 400
    
    #user owner of channel
    data = {
        'token' : token_generate(1, 'login'),
        'message_id' : 10001,
    }
    resp = requests.delete(url + 'message/remove', json = data)
    assert resp.status_code == 200

def test_remove_invalid_token(url, initial_conditions):
    data = {
        'token' : token_generate(1, 'logout'),
        'message_id' : 10001,
    }
    resp = requests.delete(url + 'message/remove', json = data)
    assert resp.status_code == 400
    
### MESSAGE EDIT TESTS

def test_edit_standard(url, initial_conditions):
    #standard edit
    # not-empty new msg
    data = {
        'token' : token_generate(1, 'login'),
        'message_id' : 10001,
        'message' : 'new message',
    }
    resp = requests.put(url + 'message/edit', json = data)
    assert resp.status_code == 200
    msg_data = {
        'token' : token_generate(1, 'login'),
        'channel_id' : 1,
        'start' : 0,
    }
    resp = requests.get(url + 'channel/messages', params=msg_data)
    assert len(json.loads(resp.text)['messages']) == 4
    # empty new msg
    data['message'] = ''
    resp = requests.put(url + 'message/edit', json = data)
    assert resp.status_code == 200
    resp = requests.get(url + 'channel/messages', params=msg_data)
    assert len(json.loads(resp.text)['messages']) == 3

def test_edit_messageid(url, initial_conditions):
    # incorrect message_id
    data = {
        'token' : token_generate(5, 'login'),
        'message_id' : 10002,
        'message' : 'new message',
    }
    resp = requests.put(url + 'message/edit', json = data)
    assert resp.status_code == 400
    # correct message_id
    data = {
        'token' : token_generate(2, 'login'),
        'message_id' : 10002,
        'message' : 'new message',
    }
    resp = requests.put(url + 'message/edit', json = data)
    assert resp.status_code == 200
    
def test_edit_not_an_owner(url, initial_conditions):
    #user not an owner
    data = {
        'token' : token_generate(3, 'login'),
        'message_id' : 10003,
        'message' : 'new message',
    }
    resp = requests.put(url + 'message/edit', json = data)
    assert resp.status_code == 400
    #user is owner
    data = {
        'token' : token_generate(2, 'login'),
        'message_id' : 10002,
        'message' : 'new message',
    }
    resp = requests.put(url + 'message/edit', json = data)
    assert resp.status_code == 200

def test_edit_invalid_token(url, initial_conditions):
    data = {
        'token' : token_generate(1, 'logout'),
        'message_id' : 10001,
        'message' : 'new message',
    }
    
    resp = requests.put(url + 'message/edit', json = data)
    assert resp.status_code == 400

### message sendlater tests
def test_sendlater_standard(url, initial_conditions):
    #standard send
    data = {
        'token' : token_generate(1, 'login'),
        'channel_id' : 1,
        'message' : 'This is the first message.',
        'time_sent' : time.time() + 10,
    }
    resp = requests.post(url + 'message/sendlater', json = data)
    assert resp.status_code == 200
    
    
