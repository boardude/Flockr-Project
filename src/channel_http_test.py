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

#####################
###CHANNEL DETAILS###
#####################
def http_test_chennel_valid_details(url, initial_users):
    '''
        valid test
        register user1 and create channel1
        register user2 and create channel2
        register user3 and join channel1
        user1 requests channel_details for channel1
        user2 requests channel_details for channel2
    '''
    input = {
        'email' : '1test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    token1 = json.loads(resp.text)['token']
    u1_id = json.loads(resp.text)['u_id']
    input = {
        'email' : '2test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    token2 = json.loads(resp.text)['token']
    u2_id = json.loads(resp.text)['u_id']
    input = {
        'email' : '3test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    u3_id = json.loads(resp.text)['u_id']

    ###user 1 create channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']

    ###user 2 create channel2
    input = {
        'token' : token2,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id2 = json.loads(resp.text)['channel_id']

    ###user 1 invite user3
    input = {
        'token' : token1,
        'channel_id' : channel_id1,
        'u_id' : u3_id
    }
    requests.post(url + 'channel/invite', json=input)

    ###user 1 require channel details
    resp = requests.get(url + 'channel/details', json={
        'token' : token1,
        'channel_id' : channel_id1
    })
    details_1 = json.loads(resp.text)
    assert details_1.status_code == 200
    assert details_1['name'] == 'channel_name_1'
    assert len(details_1['owner_members']) == 1
    assert details_1['owner_members'][0]['u_id'] == u1_id
    assert len(details_1['all_members']) == 2
    assert details_1['all_members'][0]['u_id'] == u1_id
    assert details_1['all_members'][1]['u_id'] == u3_id

    ###user 2 require channel details
    resp = requests.get(url + 'channel/details', json={
        'token' : token2,
        'channel_id' : channel_id2
    })
    details_2 = json.loads(resp.text)
    assert details_2.status_code == 200
    assert details_2['name'] == 'channel_name_2'
    assert len(details_2['owner_members']) == 1
    assert details_2['owner_members'][0]['u_id'] == u2_id
    assert len(details_2['all_members']) == 1
    assert details_2['all_members'][0]['u_id'] == u2_id

def http_test_details_invalid_channel(url, initial_users):
    '''
        invalid test of worng channel id
        register user1
        user1 create a channel
        user1 requests channel_details by wrong channel_id
    '''
    ### login a user
    input = {
        'email' : '1test@test.com',
        'password' : 'password'
    }
    resp = requests.post(url + 'auth/login', json=input)
    token1 = json.loads(resp.text)['token']
    ### user1 create channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    ###user1 require channel details with wrong channel id
    resp = requests.get(url + 'channel/details', json={
        'token' : token1,
        'channel_id' : channel_id1 + 1
    })
    assert resp.status_code == 400

def http_test_details_not_authorised_menber():
    '''
        invalid test of the authorised user is not a member of channel
        register user1 and user2
        user1 create a channel1
        user2 requests channel_details of channel1
    '''
    ##login two users
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

    ###user 1 create channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']

    ###user2 require channel details who is not an owner
    resp = requests.get(url + 'channel/details', json={
        'token' : token2,
        'channel_id' : channel_id1
    })
    assert resp.status_code == 400

    ###user with invalid token requires channel details
    resp = requests.get(url + 'channel/details', json={
        'token' : 'invalid_token',
        'channel_id' : channel_id1
    })
    assert resp.status_code == 400

################################
###HTTP TEST OF CHANNEL LEAVE###
################################
def http_test_channel_leave_member_valid():
    '''
        valid test
        regiser user1 and user2
        user1 create a new channel and invite user2
        then user2 leave the channel
    '''
    ##login two users
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
    u2_id = json.loads(resp.text)['u_id']
    token2 = json.loads(resp.text)['token']

    ###user 1 create channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    ###user 1 invite user2
    input = {
        'token' : token1,
        'channel_id' : channel_id1,
        'u_id' : u2_id
    }
    requests.post(url + 'channel/invite', json=input)

    ### user2 leave channel1
    input = {
        'token': token2,
        'channel_id' : channel_id1,
    }
    resp = requests.post(url + 'channel/leave', json=input)
    assert resp.status_code == 200

def http_test_channel_leave_owner_valid(url, initial_users):
    '''
        valid test
        regiser user1 and user2
        user1 create a new channel and invite user2
        then user1 leave the channel
    '''
    ##login two users
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
    u2_id = json.loads(resp.text)['u_id']


    ###user 1 create channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    ###user 1 invite user2
    input = {
        'token' : token1,
        'channel_id' : channel_id1,
        'u_id' : u2_id
    }
    requests.post(url + 'channel/invite', json=input)

    ### user1 who is the owner leave channel1
    input = {
        'token': token1,
        'channel_id' : channel_id1,
    }
    resp = requests.post(url + 'channel/leave', json=input)
    assert resp.status_code == 200
def http_test_channel_leave_invalid_channel_id(url, initial_users):
    '''
        "test_leave_inputerror_channel"
        invalid test of channel id is not a valid
        regiser user1 and user2
        user1 create a new channel and invite user2
        then user2 leave channel with wrong channel_id
    '''
    ##login two users
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
    u2_id = json.loads(resp.text)['u_id']
    token2 = json.loads(resp.text)['token']

    ###user 1 create channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    ###user 1 invite user2
    input = {
        'token' : token1,
        'channel_id' : channel_id1,
        'u_id' : u2_id
    }
    requests.post(url + 'channel/invite', json=input)

    ### user2 leave channel1 with wrong channel id
    input = {
        'token': token2,
        'channel_id' : channel_id1 + 1
    }
    resp = requests.post(url + 'channel/leave', json=input)
    assert resp.status_code == 400

def http_test_channel_leave_not_authorised_member():
    '''
        change function name from "test_leave_AccessError_not_authorised_member"
        to "test_leave_accesserror_not_authorised_member"
        invalid test of the authorised user is not already a member of t he channel
        register user1 and user2
        user1 create a new channel and DO NOT invite user2
        user2 leave channel with user1's channel_id
    '''
    ##login two users
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

    ###user 1 create channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    ### user2 leave channel1 with wrong channel id
    input = {
        'token': token2,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/leave', json=input)
    assert resp.status_code == 400
    ### invalid test if the token does not refer to a valid user
    input = {
        'token': 'invalidtoken',
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/leave', json=input)
    assert resp.status_code == 400


################################
###HTTP TEST OF CHANNEL JOIN ###
################################
def http_test_channel_join_default_user_valid(url, initial_users):
    '''
        valid test
        register user1 and user2
        user1 create a public channel
        user2 join that channel
    '''
    ##login two users
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

    ###user 1 create channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    ### user2 join channel1
    input = {
        'token': token2,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    assert resp.status_code == 200

    ###user1 who is the owner join the channel
    input = {
        'token': token1,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    assert resp.status_code == 200

    ###user 2 join the channel again
    input = {
        'token': token2,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    assert resp.status_code == 200

def http_test_channel_join_folckr_owner(url, initial_users):
    '''
        valid test
        register user1 and user2
        user2 create a private channel
        user1 join that channel
    '''
    ##login two users
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
    ###user 2 create private channel1
    input = {
        'token' : token2,
        'name' : 'channel_name',
        'public' : False
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    ### user1 join channel1
    input = {
        'token': token1,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    assert resp.status_code == 200

def http_test_channel_join_incorrect_channel_id(url, initial_users):
    '''
        "test_join_inputerror_channel"
        invalid test of the invalid channel ID
        register user1 and user2
        user1 create a public channel
        user2 join channel with wrong channel_id
    '''
    ##login two users
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

    ###user 1 create channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    ### user2 join channel1
    input = {
        'token': token2,
        'channel_id' : channel_id1 + 1
    }
    resp = requests.post(url + 'channel/join', json=input)
    assert resp.status_code == 400

def http_test_channel_join_not_public(url, initial_users):
    '''
        invalid test of the private channel
        register user1 and user2
        user1 create a NOT-public channel
        user2 join that channel
    '''
    ##login two users
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
    ###user 1 create private channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : False
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    ### user2 join channel1
    input = {
        'token': token2,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    assert resp.status_code == 400

####################################
###HTTP TEST OF CHANNEL ADDOWNER ###
####################################
def http_test_channel_addowner_valid(url, initial_users):
    '''
        valid test
    '''
    ##login two users
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
    u2_id = json.loads(resp.text)['u_id']
    
    ###user 1 create public channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    
    ### user2 join channel1
    input = {
        'token': token2,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    
    ###user1 add user2 as a new owner
    input = {
        'token': token1,
        'channel_id' : channel_id1,
        'u_id': u2_id
    }
    resp = requests.post(url + 'channel/addowner', json=input)
    assert resp.status_code == 200

def http_test_channel_addwoner_invalid_channel_id(url, initial_users):
    '''
        "test_addowner_inputerror_invalid_channel"
        invalid test of wrong channel id
        register user1 and user2
        user1 invites user2
        user1 add user2 as an owner with invalid channel id
    '''
    ##login two users
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
    u2_id = json.loads(resp.text)['u_id']
    token2 = json.loads(resp.text)['token']
    
    ###user 1 create public channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']
    
    ### user2 join channel1
    input = {
        'token': token2,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    
    ###user1 add user2 as a new owner
    input = {
        'token': token1,
        'channel_id' : channel_id1 + 1,
        'u_id': u2_id
    }
    resp = requests.post(url + 'channel/addowner', json=input)
    assert resp.status_code == 400

def http_test_channel_addowner_already_owner(url, initial_users):
    '''
        invalid test of user is already an owner of the channel
    '''
    ##login two users
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
    u2_id = json.loads(resp.text)['u_id']
    
    ###user 1 create public channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']

    ### user2 join channel1
    input = {
        'token': token2,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    
    ###user1 add user2 as a new owner
    input = {
        'token': token1,
        'channel_id' : channel_id1,
        'u_id': u2_id
    }
    requests.post(url + 'channel/addowner', json=input)
    
    ###addowner twice
    resp = requests.post(url + 'channel/addowner', json=input)
    assert resp.status_code == 400

def http_test_channel_addowner_not_owner():
    ##login three users
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
    u3_id = json.loads(resp.text)['u_id']
    token3 = json.loads(resp.text)['token']
    ###user 1 create public channel1
    input = {
        'token' : token1,
        'name' : 'channel_name',
        'public' : True
    }
    resp = requests.post(url + 'channels/create', json=input)
    channel_id1 = json.loads(resp.text)['channel_id']

    ### user2 user3 join channel1
    input = {
        'token': token2,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    input = {
        'token': token3,
        'channel_id' : channel_id1
    }
    resp = requests.post(url + 'channel/join', json=input)
    ###user2 who is not owner add user3 as a new owner
    input = {
        'token': token2,
        'channel_id' : channel_id1,
        'u_id': u3_id
    }
    resp = requests.post(url + 'channel/addowner', json=input)
    assert resp.status_code == 400
