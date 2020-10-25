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
def create_users():
    # clear data
    requests.delete(url + 'clear')

    # register & log in 3 users
    for i in range(3):
        user_data = {
            'password' : 'validpass' + str(i),
            'name_first': 'User',
            'name_last' : '0' + str(i),
            'email': 'validuser' + str(i) + '@gmail.com',
        }
        requests.post(url + 'auth/register', json=user_data)
        resp = requests.post(url + 'auth/login', json=user_data)

def test_http_userpermission_InputError(url, create_users):
    # u_id does not refer to a valid user
    query = {
        'token': token_generate(1, 'login'),
        'u_id': 0,
        'permission_id': 1,
    }
    r = requests.post(url + 'admin/userpermission/change', json=query)
    assert r.status_code == 400

    # permission_id does not refer to a value permission
    query = {
        'token': token_generate(1, 'login'),
        'u_id': 2,
        'permission_id': 3,
    }
    r = requests.post(url + 'admin/userpermission/change', json=query)
    assert r.status_code == 400

    # permission_id does not refer to a value permission (wrong data type)
    query = {
        'token': token_generate(1, 'login'),
        'u_id': 2,
        'permission_id': 'str',
    }
    r = requests.post(url + 'admin/userpermission/change', json=query)
    assert r.status_code == 400

def test_http_userpermission_AccessError(url, create_users):
    # token is not an authorised user
    bad_token = 'invalid_token'
    query = {
        'token': bad_token,
        'u_id': 1,
        'permission_id': 2,
    }
    r = requests.post(url + 'admin/userpermission/change', json=query)
    assert r.status_code == 400

    # token is an authorised user but not an owner
    query = {
        'token': token_generate(2, 'login'),
        'u_id': 1,
        'permission_id': 2,
    }
    r = requests.post(url + 'admin/userpermission/change', json=query)
    assert r.status_code == 400

def test_http_userpermission_standard(url, create_users):
    query = {
        'token': token_generate(1, 'login'),
        'u_id': 2,
        'permission_id': 1,
    }
    r = requests.post(url + 'admin/userpermission/change', json=query)
    assert r.status_code == 200

    query = {
        'token': token_generate(1, 'login'),
        'u_id': 3,
        'permission_id': 1,
    }
    r = requests.post(url + 'admin/userpermission/change', json=query)
    assert r.status_code == 200

    query = {
        'token': token_generate(2, 'login'),
        'u_id': 3,
        'permission_id': 2,
    }
    r = requests.post(url + 'admin/userpermission/change', json=query)
    assert r.status_code == 200

    query = {
        'token': token_generate(2, 'login'),
        'u_id': 1,
        'permission_id': 2,
    }
    r = requests.post(url + 'admin/userpermission/change', json=query)
    assert r.status_code == 200

def test_http_clear_standard(url):
    r = requests.delete(url + 'clear')
    assert r.status_code == 200

def test_http_search_invalid_token(url, create_users):
    # empty
    r = requests.get(url + 'search', params={'token': ''})
    assert r.status_code == 400

    # None
    r = requests.get(url + 'search', params={'token': None})
    assert r.status_code == 400

    # Not the correct data type
    r = requests.get(url + 'search', params={'token': 123})
    assert r.status_code == 400

    # Not an authorised user
    bad_token = 'invalid_token'
    r = requests.get(url + 'search', params={'token': bad_token})
    assert r.status_code == 400

def test_http_search_standard(url, create_users):
    # create a channel from user 1
    query = {
        'token': token_generate(1, 'login'),
        'channel_name': 'Chanenl 01 User 01',
        'is_public': True,
    }
    r = requests.post(url + 'channels/create', json=query)
    payload = r.json()

    # user 2 joins user 1's cannel
    query = {
        'token': token_generate(2, 'login'),
        'channel_id': payload['channel_id'],
    }
    r = requests.post(url + 'channels/join', json=query)

    # send messages from both users
    query = {
        'token': token_generate(1, 'login'),
        'channel_id': payload['channel_id'],
        'message': 'What\'s up user two',
    }
    r = requests.post(url + 'message/send', json=query)
    msg1 = r.json()

    query = {
        'token': token_generate(2, 'login'),
        'channel_id': payload['channel_id'],
        'message': 'What\'s up user one',
    }
    r = requests.post(url + 'message/send', json=query)
    msg2 = r.json()

    query = {
        'token': token_generate(2, 'login'),
        'channel_id': payload['channel_id'],
        'message': 'You user one or What?',
    }
    r = requests.post(url + 'message/send', json=query)
    msg3 = r.json()

    query = {
        'token': token_generate(1, 'login'),
        'channel_id': payload['channel_id'],
        'message': 'What? Yeah I am',
    }
    r = requests.post(url + 'message/send', json=query)
    msg4 = r.json()

    query = {
        'token': token_generate(2, 'login'),
        'channel_id': payload['channel_id'],
        'message': 'What?',
    }
    r = requests.post(url + 'message/send', json=query)
    msg5 = r.json()

    # search from first user
    query = {
        'token': token_generate(1, 'login'),
        'query_str': 'What',
    }
    r = requests.post(url + 'search', params=query)
    assert r.status_code == 200

    # make sure messages from both users are returned
    payload = r.json()
    assert len(payload['messages']) == 5
    assert payload['messages'][0]['message_id'] == msg1['message_id']
    assert payload['messages'][0]['u_id'] == 1
    assert payload['messages'][0]['message'] == 'What\'s up user two'
    assert payload['messages'][1]['message_id'] == msg2['message_id']
    assert payload['messages'][1]['u_id'] == 2
    assert payload['messages'][1]['message'] == 'What\'s up user one'
    assert payload['messages'][2]['message_id'] == msg3['message_id']
    assert payload['messages'][2]['u_id'] == 2
    assert payload['messages'][2]['message'] == 'You user one or What?'
    assert payload['messages'][3]['message_id'] == msg4['message_id']
    assert payload['messages'][3]['u_id'] == 1
    assert payload['messages'][3]['message'] == 'What? Yeah I am'
    assert payload['messages'][4]['message_id'] == msg5['message_id']
    assert payload['messages'][4]['u_id'] == 2
    assert payload['messages'][4]['message'] == 'What?'

def test_http_users_all_invalid_token(url, create_users):
    # empty
    r = requests.get(url + 'users/all', params={'token': ''})
    assert r.status_code == 400

    # None
    r = requests.get(url + 'users/all', params={'token': None})
    assert r.status_code == 400

    # Not the correct data type
    r = requests.get(url + 'users/all', params={'token': 123})
    assert r.status_code == 400

    # Not an authorised user
    bad_token = 'invalid_token'
    r = requests.get(url + 'users/all', params={'token': bad_token})
    assert r.status_code == 400

def test_http_users_all_standard(url, create_users):
    r = requests.get(url + 'users/all', params={'token': token_generate(1, 'login')})
    payload = r.json()

    # check correct details have been returned
    assert payload['users'][0]['u_id'] == users[0]['u_id']
    assert payload['users'][0]['email'] == 'validuseremail@gmail.com'
    assert payload['users'][0]['name_first'] == 'User'
    assert payload['users'][0]['name_last'] == 'One'
    assert payload['users'][0]['handle_str'] == 'userone'

    assert payload['users'][1]['u_id'] == users[1]['u_id']
    assert payload['users'][1]['u_id'] == users[1]['u_id']
    assert payload['users'][1]['email'] == 'validuser2email@gmail.com'
    assert payload['users'][1]['name_first'] == 'User'
    assert payload['users'][1]['name_last'] == 'Two'
    assert payload['users'][1]['handle_str'] == 'usertwo'

    assert payload['users'][2]['u_id'] == users[2]['u_id']
    assert payload['users'][2]['email'] == 'validuser3email@gmail.com'
    assert payload['users'][2]['name_first'] == 'User'
    assert payload['users'][2]['name_last'] == 'Three'
    assert payload['users'][2]['handle_str'] == 'userthree'
