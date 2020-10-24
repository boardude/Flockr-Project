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

def http_test_user_profile(url):
    '''
        vlaid test
        register and login user1
        test for returned details
    '''

    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    #register a user with input1
    requests.post(url + 'auth/register', json=input1)

    #login the user with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return = json.loads(login_resp1.text)

    #get token and u_id from login
    input2 = {
        'token': login_return['token'],
        'u_id' : login_return['u_id']
    }

    #user the token and u_id to check user/profile
    resp2 = requests.get(url + 'user/profile', json=input2)
    assert resp2.status_code == 200
    assert json.loads(resp2.text)['user']['u_id'] == input2['u_id']
    assert json.loads(resp2.text)['user']['email'] == 'test1@test.com'
    assert json.loads(resp2.text)['user']['name_first'] == 'user1_name'
    assert json.loads(resp2.text)['user']['name_last'] == 'user1_name'

def http_test_invalid_uid(url):
    '''
        invalid uid to check:
            1. call clear to clear all data
            2. call auth/register and auth/login to get 'login and register'
            3. give user1's u_id to check user2 profile
    '''
    #give a clear function to clear all the data
    requests.delete(url + 'clear')

    #register a user with input1
    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login the user with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return1 = json.loads(login_resp1.text)

    #get the u_id and token from user1
    input2 = {
        'token' : login_return1['token'],
        'u_id': login_return1['u_id']
    }

    #register second user with input3
    input3 = {
        'email' : 'test2@test.com',
        'password' : 'passowrd',
        'name_first' : 'user2_name',
        'name_last' : 'user2_name'
    }
    requests.post(url + 'auth/register', json=input3)
    login_resp2 = requests.post(url + 'auth/login', json={
        'email' : 'test2@test.com', 'password':'password'})
    login_return2 = json.loads(login_resp2.text)

    #get the u_id and token from user2
    input4 = {
        'token': login_return2['token'],
        'u_id': login_return2['u_id']
    }

    #call the user/profile with user1's token and user2's u_id
    profile_resp = requests.get(url + 'user/profile', json={
        'token': input2['token'], 'u_id': input4['u_id']})
    assert profile_resp.status_code == 400
