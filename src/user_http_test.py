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
###########################
###HTTP TEST of SETNAME ###
###########################

def http_test_valid_setname(url):
    '''
        valid test:
            1. call clear to claear all data
            2. call auth/register and auth/login to get 'login and register'
            3. call setname to reset name
            4. call user/profile to check accuracy

    '''
    requests.delete(url + 'clear')
    ###normal test for setname###

    #register user1 with input1
    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login user1 with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password':'password'})
    login_return1 = json.loads(login_resp1.text)

    #reset user1 name with input2
    input2 = {
        'token': login_return1['token'],
        'name_first': 'first_name',
        'name_last': 'last_name'
    }
    requests.put(url + 'user/profile/setname', json=input2)

    #checke user/prifile with input3
    input3 = {
        'token': login_return1['token'],
        'u_id' : login_return1['u_id']
    }
    resp1 = requests.get(url + 'user/profile', json=input3)
    assert resp1.status_code == 200
    assert json.loads(resp1.text)['user']['name_first'] == input2['name_first']
    assert json.loads(resp1.text)['user']['name_last'] == input2['name_last']

    ###http test for length 50###

    #register user2 with input4
    input4 = {
        'email' : 'test2@test.com',
        'password' : 'passowrd',
        'name_first' : 'user2_name',
        'name_last' : 'usee2_name'
    }
    requests.post(url + 'auth/register', json=input4)

    #login user2 with email and password
    login_resp2 = requests.post(url + 'auth/login', json={
        'email' : 'test2@test.com', 'password': 'password'})
    login_return2 = json.loads(login_resp2.text)

    #reset user2 name with input4
    long_name = '0123456789'
    long_name = long_name * 5
    input5 = {
        'token': login_return2['token'],
        'name_first': long_name,
        'name_last': long_name
    }
    requests.put(url + 'user/profile/setname', json=input5)

    #checke user/prifile with input5
    input6 = {
        'token': login_return2['token'],
        'u_id': login_return2['u_id']
    }
    resp2 = requests.get(url + 'user/profile', json=input6)
    assert resp2.status_code == 200
    assert json.loads(resp2.text)['user']['name_first'] == input5['name_first']
    assert json.loads(resp2.text)['user']['name_last'] == input5['name_last']

    ###http test for length 1###

    #register user3 with input7
    input7 = {
        'email' : 'test3@test.com',
        'password' : 'passowrd',
        'name_first' : 'user3_name',
        'name_last' : 'usee3_name'
    }
    requests.post(url + 'auth/register', json=input7)

    #login user3 with email and password
    login_resp3 = requests.post(url + 'auth/login', json={
        'email' : 'test3@test.com', 'password': 'password'})
    login_return3 = json.loads(login_resp3.text)

    #reset user3 name with input8
    input8 = {
        'token': login_return3['token'],
        'name_first': '1',
        'name_last': '1',
    }
    requests.put(url + 'user/profile/setname', json=input8)

    #checke user/prifile with input9
    input9 = {
        'token': login_return3['token'],
        'u_id' : login_return2['u_id']
    }
    resp3 = requests.get(url + 'user/profile', json=input9)
    assert resp3.status_code == 200
    assert json.loads(resp3.text)['user']['name_first'] == input8['name_first']
    assert json.loads(resp3.text)['user']['name_last'] == input8['name_last']

def http_test_invalid_firstname(url):
    '''
        invalid test of 0 characters and 26 charaters of firstname
    '''
    requests.delete(url + 'clear')

    #register user1 with input1
    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login user1 with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return1 = json.loads(login_resp1.text)

    #reset long name for user
    long_name = '012345678910'
    long_name = long_name * 5
    #reset user1 name with input2
    input2 = {
        'token': login_return1['token'],
        'name_first': long_name,
        'name_last': 'last_name',
    }
    requests.put(url + 'user/profile/setname', json=input2)

    #checke user/prifile with input3 for user1
    input3 = {
        'token': login_return1['token'],
        'u_id' : login_return1['u_id']
    }
    resp1 = requests.get(url + 'user/profile', json=input3)
    assert resp1.status_code == 400

    #reset zero characters for user
    input4 = {
        'token': login_return1['token'],
        'name_first': '',
        'name_last': 'last_name',
    }
    resp2 = requests.put(url + 'user/profile/setname', json=input4)

    assert resp2.status_code == 400

def http_test_invalid_lastname(url):
    '''
        invalid test of 0 characters and 26 charaters of firstname
    '''
    requests.delete(url + 'clear')

    #register user1 with input1
    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login user1 with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return1 = json.loads(login_resp1.text)

    #reset long name for user
    long_name = '012345678910'
    long_name = long_name * 5
    #reset user1 name with input2
    input2 = {
        'token': login_return1['token'],
        'name_first': 'first_name',
        'name_last': long_name,
    }
    resp1 = requests.put(url + 'user/profile/setname', json=input2)
    assert resp1.status_code == 400

    #reset zero characters for user
    input4 = {
        'token': login_return1['token'],
        'name_first': 'first_name',
        'name_last': '',
    }
    resp2 = requests.put(url + 'user/profile/setname', json=input4)
    assert resp2.status_code == 400

###########################
###HTTP TEST of SETEMAIL###
###########################

def http_test_profile_setemail_valid(url):
    '''
        invalid test of 0 characters and 26 charaters of firstname
    '''
    requests.delete(url + 'clear')

    #register user1 with input1
    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login user1 with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return1 = json.loads(login_resp1.text)

    #reset email for user
    input2 = {
        'token': login_return1['token'],
        'email': 'email@test.com'
    }
    resp = requests.put(url + 'user/profile/setemail', json=input2)
    assert resp.status_code == 200
    #checke user/prifile with input3 for user1
    input3 = {
        'token': login_return1['token'],
        'u_id' : login_return1['u_id']
    }
    resp1 = requests.get(url + 'user/profile', json=input3)
    assert resp1.status_code == 200
    assert json.loads(resp1)['user']['email'] == input2['email']

def http_test_profile_setemail_incorrect(url):
    '''
        invalid test of incorrect email format
    '''
    requests.delete(url + 'clear')

    #register user1 with input1
    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login user1 with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return1 = json.loads(login_resp1.text)

    #reset user1 name with input2
    input2 = {
        'token': login_return1['token'],
        'email': 'emailtest.com'
    }
    requests.put(url + 'user/profile/setemail', json=input2)

    #checke user/prifile with input3 for user1
    input3 = {
        'token': login_return1['token'],
        'u_id' : login_return1['u_id']
    }
    resp1 = requests.get(url + 'user/profile', json=input3)
    assert resp1.status_code == 400

#############################
###HTTP TEST OF SETHANDLE ###
#############################

def http_test_handle_valid(url):
    '''
    valid test for sethandle
    '''
    requests.delete(url + 'clear')
    ###normal test for sethandle###

    #register user1 with input1
    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login user1 with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return1 = json.loads(login_resp1.text)

    #reset user1 handle with input2
    input2 = {
        'token': login_return1['token'],
        'handle_str': 'updatename'
    }
    resp = requests.put(url + 'user/profile/sethandle', json=input2)
    assert resp.status_code == 200
    #checke user/prifile with input3
    input3 = {
        'token': login_return1['token'],
        'u_id' : login_return1['u_id']
    }
    resp1 = requests.get(url + 'user/profile', json=input3)
    assert resp1.status_code == 200
    assert json.loads(resp1)['user']['handle_str'] == input2['handle_str']

    ###http test for length 20###

    #register user2 with input4
    input4 = {
        'email' : 'test2@test.com',
        'password' : 'passowrd',
        'name_first' : 'user2_name',
        'name_last' : 'usee2_name'
    }
    requests.post(url + 'auth/register', json=input4)

    #login user2 with email and password
    login_resp2 = requests.post(url + 'auth/login', json={
        'email' : 'test2@test.com', 'password': 'password'})
    login_return2 = json.loads(login_resp2.text)

    #reset user2 email with input5
    input5 = {
        'token': login_return2['token'],
        'handle_str': '12345678911234567891'
    }
    resp = requests.put(url + 'user/profile/sethandle', json=input5)
    assert resp.status_code == 200
    #checke user/prifile with input6
    input6 = {
        'token': login_return2['token'],
        'u_id' : login_return2['u_id']
    }
    resp2 = requests.get(url + 'user/profile', json=input6)
    assert resp2.status_code == 200
    assert json.loads(resp2)['user']['handle_str'] == input5['handle_str']
    ###http test for length 3###

    #register user3 with input6
    input7 = {
        'email' : 'test3@test.com',
        'password' : 'passowrd',
        'name_first' : 'user3_name',
        'name_last' : 'usee3_name'
    }
    requests.post(url + 'auth/register', json=input7)

    #login user3 with email and password
    login_resp3 = requests.post(url + 'auth/login', json={
        'email' : 'test3@test.com', 'password': 'password'})
    login_return3 = json.loads(login_resp3.text)

    #reset user3 name with input8
    input8 = {
        'token': login_return3['token'],
        'hanlde_str': 'abc'
    }
    resp = requests.put(url + 'user/profile/sethandle', json=input8)
    assert resp.status_code == 200
    #checke user/prifile with input8
    input9 = {
        'token': login_return3['token'],
        'u_id' : login_return2['u_id']
    }
    resp3 = requests.get(url + 'user/profile', json=input9)
    assert resp3.status_code == 200
    assert json.loads(resp3)['user']['handle_str'] == input8['handle_str']

def http_test_handle_incorrect_length(url):
    '''
        incorrect length test for reset handle
    '''
    requests.delete(url + 'clear')

    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login user1 with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return1 = json.loads(login_resp1.text)

    handle_reps1 = requests.post(url + 'user/profile/sethandle', json={
        'token': login_return1['token'], 'handle_str': 'u'})
    assert handle_reps1.status_code == 400

    handle_reps2 = requests.post(url + 'user/profile/sethandle', json={
        'token': login_return1['token'], 'handle_str': 'abcdefghijklmnopkistuvwxyz'})
    assert handle_reps2.status_code == 400

    handle_reps1 = requests.post(url + 'user/profile/sethandle', json={
        'token': login_return1['token'], 'handle_str': ''})
    assert handle_reps1.status_code == 400

    handle_reps1 = requests.post(url + 'user/profile/sethandle', json={
        'token': login_return1['token'], 'handle_str': '12'})
    assert handle_reps1.status_code == 400

def http_test_handle_being_used(url):
    '''
        invalid test for the handle has being used
    '''
    requests.delete(url + 'clear')

    #register user1 with input1
    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login user1 with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return1 = json.loads(login_resp1.text)

    #register user2 with input2
    input2 = {
        'email' : 'test2@test.com',
        'password' : 'passowrd',
        'name_first' : 'user2_name',
        'name_last' : 'usee2_name'
    }
    requests.post(url + 'auth/register', json=input2)

    #login user2 with email and password
    login_resp2 = requests.post(url + 'auth/login', json={
        'email' : 'test2@test.com', 'password': 'password'})
    login_return2 = login_resp2.json()

    temp1_handle_str = requests.get(url + 'user/profile', json={
        'u_id' : login_return1['u_id'], 'token': login_return1['token']})['handle_str']
    temp2_handle_str = requests.get(url + 'user/profile', json={
        'u_id' : login_return2['u_id'], 'token': login_return2['token']})['handle_str']

    handle_resp1 = requests.put(url + 'user/profile/sethandle', json={
        'token': login_return1['token'], 'handle_str': temp2_handle_str})
    handle_resp2 = requests.put(url + 'user/profile/sethandle', json={
        'token': login_return2['token'], 'handle_str': temp1_handle_str})

    assert handle_resp1.status_code == 400
    assert handle_resp2.status_code == 400

def http_test_invalid_token(url):
    '''
        invalid token to check
    '''
    requests.delete(url + 'clear')

    input1 = {
        'email' : 'test1@test.com',
        'password' : 'passowrd',
        'name_first' : 'user1_name',
        'name_last' : 'user1_name'
    }
    requests.post(url + 'auth/register', json=input1)

    #login user1 with email and password
    login_resp1 = requests.post(url + 'auth/login', json={
        'email' : 'test1@test.com', 'password': 'password'})
    login_return1 = json.loads(login_resp1.text)
    token_reps1 = requests.get(url + 'user/profile', json={
        'token': 'invalidtoken', 'u_id': login_return1['u_id']})
    assert token_reps1.status_code == 400
