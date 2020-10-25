'''
    http test of user
'''

import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import pytest
from auth import token_generate
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
def initial_basics(url):
    # this function would clear all data and create 3 users
    requests.delete(url + 'clear')
    user_data = {
        'password' : 'password',
        'name_first': 'u',
        'name_last' : '1',
        }
    for idx in range(3):
        email = str(idx + 1) + 'test@test.com'
        user_data['email'] = email
        requests.post(url + 'auth/register', json=user_data)
        requests.post(url + 'auth/login', json={'email': email, 'password': 'password'})

###########################
###HTTP TEST of PROFILE ###
###########################
def test_user_profile(url, initial_basics):
    '''
        vlaid test
        register and login user1
        test for returned details
    '''

    #get token
    data = {
        'token': token_generate(1, 'login'),
        'u_id' : 1,
    }

    #user the token and u_id to check user/profile
    resp = requests.get(url + 'user/profile', params=data)
    assert resp.status_code == 200
    assert json.loads(resp.text)['user']['u_id'] == data['u_id']
    assert json.loads(resp.text)['user']['email'] == '1test@test.com'
    assert json.loads(resp.text)['user']['name_first'] == 'u'
    assert json.loads(resp.text)['user']['name_last'] == '1'

def test_profile_invalid_uid(url, initial_basics):
    '''
        invalid uid to check:
            1. call clear to clear all data
            2. call auth/register and auth/login to get 'login and register'
            3. give user1's u_id to check user2 profile
    '''
    #call the user/profile with user1's token and user2's u_id
    profile_resp = requests.get(url + 'user/profile', params={
        'token': token_generate(1, 'login'), 'u_id': 2})
    assert profile_resp.status_code == 400

def test_profile_invalid_token(url, initial_basics):
    data = {
        'token' : 'invalid_token',
        'u_id' : 1,
    }
    profile_resp = requests.get(url + 'user/profile', params=data)
    assert profile_resp.status_code == 400
    data['token'] = token_generate(1, 'logout')
    assert profile_resp.status_code == 400

###########################
###HTTP TEST of SETNAME ###
###########################

def test_valid_setname(url, initial_basics):
    '''
        valid test:
    '''
    #get token
    data = {
        'token': token_generate(1, 'login'),
        'name_first': 'first',
        "name_last": 'last',
    }
    resp = requests.put(url + 'user/profile/setname', json=data)
    assert resp.status_code == 200
    ###http test for length 50###

    long_name = '0123456789'
    long_name = long_name * 5
    data = {
        'token': token_generate(1, 'login'),
        'name_first': long_name,
        'name_last': long_name,
    }
    resp = requests.put(url + 'user/profile/setname', json=data)
    assert resp.status_code == 200

    ###http test for length 1###
    #reset user3 name with data
    data = {
        'token': token_generate(1, 'login'),
        'name_first': '1',
        'name_last': '1',
    }
    resp = requests.put(url + 'user/profile/setname', json=data)
    assert resp.status_code == 200

def test_setname_invalid_firstname(url, initial_basics):
    '''
        invalid test of 0 characters and 26 charaters of firstname
    '''

    #reset long name for user
    long_name = '0123456789' * 5 + '1'
    #reset user1 name with data
    data = {
        'token': token_generate(1, 'login'),
        'name_first': long_name,
        'name_last': 'last_name',
    }
    resp1 = requests.put(url + 'user/profile/setname', json=data)
    assert resp1.status_code == 400

    #reset zero characters for user
    data = {
        'token': token_generate(1, 'login'),
        'name_first': '',
        'name_last': 'last_name',
    }
    resp = requests.put(url + 'user/profile/setname', json=data)
    assert resp.status_code == 400

def test_set_name_invalid_lastname(url, initial_basics):
    '''
        invalid test of 0 characters and 26 charaters of firstname
    '''
    #reset long name for user
    long_name = '0123456789' * 5 + '1'
    #reset user1 name with data2
    data2 = {
        'token': token_generate(1, 'login'),
        'name_first': 'first_name',
        'name_last': long_name,
    }
    resp1 = requests.put(url + 'user/profile/setname', json=data2)
    assert resp1.status_code == 400

    #reset zero characters for user
    data4 = {
        'token': token_generate(1, 'login'),
        'name_first': 'first_name',
        'name_last': '',
    }
    resp2 = requests.put(url + 'user/profile/setname', json=data4)
    assert resp2.status_code == 400

def test_setname_invalid_token(url, initial_basics):
    data = {
        'token' : token_generate(1, 'logout'),
        'name_first' : 'first',
        'name_last' : 'last',
    }
    resp = requests.put(url + 'user/profile/setname', json=data)
    assert resp.status_code == 400
    data['token'] = 'invalid_token'
    resp = requests.put(url + 'user/profile/setname', json=data)
    assert resp.status_code == 400

###########################
###HTTP TEST of SETEMAIL###
###########################

def test_profile_setemail_valid(url, initial_basics):
    '''
        invalid test of 0 characters and 26 charaters of firstname
    '''
    #reset email for user
    data2 = {
        'token': token_generate(1, 'login'),
        'email': 'email@test.com'
    }
    resp = requests.put(url + 'user/profile/setemail', json=data2)
    assert resp.status_code == 200

def test_profile_setemail_incorrect(url, initial_basics):
    '''
        invalid test of incorrect email format
    '''
    #reset user1 name with data
    data = {
        'token': token_generate(1, 'login'),
        'email': 'emailtest.com'
    }
    resp1 = requests.put(url + 'user/profile/setemail', json=data)
    assert resp1.status_code == 400

def test_profile_setemail_occupied(url, initial_basics):
    '''
        invalid test of incorrect email format
    '''
    #reset user1 name with data
    data = {
        'token': token_generate(1, 'login'),
        'email': '2test@test.com'
    }
    resp1 = requests.put(url + 'user/profile/setemail', json=data)
    assert resp1.status_code == 400

def test_setemail_invalid_token(url, initial_basics):
    data = {
        'token' : token_generate(1, 'logout'),
        'email' : 'newemail@test.com',
    }
    resp = requests.put(url + 'user/profile/setemail', json=data)
    assert resp.status_code == 400

#############################
###HTTP TEST OF SETHANDLE ###
#############################

def test_sethandle_valid(url, initial_basics):
    '''
    valid test for sethandle
    '''
    #reset user1 handle with data
    data = {
        'token': token_generate(1, 'login'),
        'handle_str': 'updatename'
    }
    resp = requests.put(url + 'user/profile/sethandle', json=data)
    assert resp.status_code == 200

def test_handle_incorrect_length(url, initial_basics):
    '''
        incorrect length test for reset handle
    '''

    handle_reps1 = requests.put(url + 'user/profile/sethandle', json={
        'token': token_generate(1, 'login'), 'handle_str': 'u'})
    assert handle_reps1.status_code == 400

    handle_reps2 = requests.put(url + 'user/profile/sethandle', json={
        'token': token_generate(1, 'login'), 'handle_str': 'a' * 21})
    assert handle_reps2.status_code == 400

    handle_reps1 = requests.put(url + 'user/profile/sethandle', json={
        'token': token_generate(1, 'login'), 'handle_str': ''})
    assert handle_reps1.status_code == 400

    handle_reps1 = requests.put(url + 'user/profile/sethandle', json={
        'token': token_generate(1, 'login'), 'handle_str': '12'})
    assert handle_reps1.status_code == 400

def test_handle_being_used(url, initial_basics):
    '''
        invalid test for the handle has being used
        user1 set a handle and user2 set the same handle
    '''

    requests.put(url + 'user/profile/sethandle', json={
        'token': token_generate(1, 'login'), 'handle_str': 'temp1_handle_str'})

    handle_resp2 = requests.put(url + 'user/profile/sethandle', json={
        'token': token_generate(2, 'login'), 'handle_str': 'temp1_handle_str'})
    assert handle_resp2.status_code == 400

def test_sethandle_invalid_token(url, initial_basics):
    '''
        invalid token to check
    '''
    #login user1 with email and password
    data = {
        'token' : token_generate(1, 'logout'),
        'handle_str' : 'hhh',
    }
    resp = requests.put(url + 'user/profile/sethandle', json=data)
    assert resp.status_code == 400
    data['token'] = 'invalid_token'
    resp = requests.put(url + 'user/profile/sethandle', json=data)
    assert resp.status_code == 400
