import pytest
import re
from subprocess import Popen, PIPE
import signal
import requests
import json
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
        if idx == 1:
            token = json.loads(resp.text)['token']
            channel_data = {
                'token' : token,
                'name' : 'channel' + str(idx),
                'is_public' : True,
            }
            requests.post(url + 'channels/create', json=channel_data)
        else:
            input = {
                'token' : token_generate(1, 'login'),
                'channel_id' : 1,
                'message' : 'message ' + idx,
            }
            requests.posts(url + 'message/send', json = input)
            if idx == 2:
                data = {
                    'token' : token_generate(2, 'login'),
                    'channel_id' : 1,
                    'u_id' : 2,
            }
            requests.post(url + 'channel/addowner', json=data)


### MESSAGE SEND TESTS
def test_send_standard(url, initial_conditions):
    #standard send
    input = {
        'token' : token_generate(1, 'login'),
        'channel_id' : 1,
        'message' : 'This is the first message.',
    }
    resp = requests.post(url + 'message/send', json = input)
    assert resp.status_code == 200
    
def test_send_bad_message(url, initial_conditions):
    #message over 1000 characters
    input = {
        'token' : token_generate,
        'channel_id' : 1,
        'message' : 'c' * 1001,
    }
    
    resp = request.post(url + 'message/send', json = input)
    assert resp.status_code == 400

def test_send_bad_channel(url, initial_conditions):
    #incorrect channel_id
    input = {
        'token' : token_generate(1, 'login'),
        'channel_id' : 0,
        'message' : 'this shouldnt work',
    }
    
    resp = request.post(url + 'message/send', json = input)
    assert resp.status_code == 400

### MESSAGE REMOVE TESTS
def test_remove_standard(url, initial_conditions):
    #standard remove
    input = {
        'token' : token_generate(1, 'login'),
        'message_id' : 10001,
    }
    
    resp = request.delete(url + 'message/remove', json = input)
    assert resp.status_code == 200

def test_remove_message_id(url, initial_conditions):
    
    # message not sent by user
    input = {
        'token' : token_generate(1, 'login'),
        'message_id' : 10002,
    }
    
    resp = request.delete(url + 'message/remove', json = input)
    assert resp.status_code == 400
    
    # message sent by user
    
    input = {
        'token' : token_generate(2, 'login'),
        'message_id' : 10002,
    }
    
    resp = request.delete(url + 'message/remove', json = input)
    assert resp.status_code == 200

def test_remove_owner(url, initial_conditions):
    
    #user not owner of channel
    input = {
        'token' : token_generate(3, 'login'),
        'message_id' : 10003,
    }
    
    resp = request.delete(url + 'message/remove', json = input)
    assert resp.status_code == 400
    
    #user owner of channel
    input = {
        'token' : token_generate(1, 'login'),
        'message_id' : 10001,
    }
    
    resp = request.delete(url + 'message/remove', json = input)
    assert resp.status_code == 200
    
### MESSAGE EDIT TESTS

def test_edit_standard(url, initial_conditions):
    #standard edit
    input = {
        'token' : token_generate(1, 'login'),
        'message_id' : 10001,
        'message' : 'new message',
    }
    
    resp = request.put(url + 'message/edit', json = input)
    assert resp.status_code == 200

def test_edit_messageid(url, initial_conditions):
    # incorrect message_id
    input = {
        'token' : token_generate(3, 'login'),
        'message_id' : 10002,
        'message' : 'new message',
    }
    
    resp = request.put(url + 'message/edit', json = input)
    assert resp.status_code == 400
    
    # correct message_id
    input = {
        'token' : token_generate(2, 'login'),
        'message_id' : 10002,
        'message' : 'new message',
    }
    
    resp = request.put(url + 'message/edit', json = input)
    assert resp.status_code == 200
    
def test_edit_not_an_owner(url, initial_conditions):
    #user not an owner
    input = {
        'token' : token_generate(3, 'login'),
        'message_id' : 10003,
        'message' : 'new message',
    }
    
    resp = request.put(url + 'message/edit', json = input)
    assert resp.status_code == 400
    
    #user is owner
    
    input = {
        'token' : token_generate(2, 'login'),
        'message_id' : 10002,
        'message' : 'new message',
    }
    
    resp = request.put(url + 'message/edit', json = input)
    assert resp.status_code == 200
