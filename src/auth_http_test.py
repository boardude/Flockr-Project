import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from auth import auth_login, auth_logout, auth_register, token_update

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

def test_register_standard(url):
    '''
    A simple test to register standard
    '''
    # create a standard user with len(password) == 6 and
    # len(first_name) == 1 and len(last_name) == 1
    input = {
        'email' : 'test1@test.com',
        'password' : '123456',
        'name_first': 'u',
        'name_last' : '1',
        }
    resp = requests.post(url + 'auth/register', json=input)
    assert resp.status_code == 200
    assert json.loads(resp.text)['u_id'] == 1
    assert json.loads(resp.text)['token'] == token_update(1, 'register')
    
    # create a standard user with len(password) == 6 and
    # len(first_name) == 50 and len(last_name) == 50
    input = {
        'email' : 'test2@test.com',
        'password' : 'password',
        'name_first' : 'u' * 50,
        'name_last' : '2' * 50,
        }
    resp = requests.post(url + 'auth/register', json=input)
    assert resp.status_code == 200
    assert json.loads(resp.text)['u_id'] == 2
    assert json.loads(resp.text)['token'] == token_update(2, 'register')

def test_register_error_invalid_email(url):
    '''
    A simple test for error when invalid email
    '''
    requests.delete(url + 'clear')
    input = {
        'email' : 'testtest.com',
        'password' : 'password',
        'name_first' : 'u',
        'name_last' : '1',
        }
    resp = requests.post(url + 'auth/register', json=input)
    assert resp.status_code == 400

def test_register_error_occupied_email(url):
    '''
    A simple test for error when occupied email
    '''
    requests.delete(url + 'clear')
    input = {
        'email' : 'test@test.com',
        'password' : 'password',
        'name_first' : 'u',
        'name_last' : '1',
        }
    resp = requests.post(url + 'auth/register', json=input)
    assert resp.status_code == 200
    resp = requests.post(url + 'auth/register', json=input)
    assert resp.status_code == 400

def test_register_error_invalid_name(url):
    '''
    A simple test for error when enterring invalid names
    '''
    requests.delete(url + 'clear')
    input = {
        'email' : 'test@test.com',
        'password' : 'password',
        'name_first' : '',
        'name_last' : '',
        }
    resp = requests.post(url + 'auth/register', json=input)
    assert resp.status_code == 400
    input['name_first'] = 'a' * 51
    resp = requests.post(url + 'auth/register', json=input)
    assert resp.status_code == 400
    input['name_last'] = 'a' * 51
