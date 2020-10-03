import auth
from other import clear
from error import InputError
import pytest
from data import *


''' Tests:
        register:
            1. email validity
            2. email already used
            2. password validity
            3. name_first validity
            4. name_last validity
        login:
            1. email exists in data
            2. password incorrect
        logout:
            1. correct return
        data:
            1. elements correct
            2. user id in ascending order
            3. handle < 20 characters
            4. bighandle < 20 character
'''

def test_register_email():
    # invalid email
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('invalidemail.com', 'valid123', 'valid', 'valid')
    
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('invalidemail', 'valid123', 'valid', 'valid')
    
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('invalidemail@com', 'valid123', 'valid', 'valid')
    
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('invalidemail@.com', 'valid123', 'valid', 'valid')
    # already used email
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
        
def test_register_password():
    # password under 6 characters
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'inval', 'valid', 'valid')
    # no password
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '', 'valid', 'valid')
    # valid password
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    auth.auth_login('validemail@gmail.com', 'valid123')
    
def test_register_namefirst():
    # no first name
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', '', 'valid')
    # first name more than 50 characters
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', '012345678901234567890123456789012345678901234567890', 'valid')
        
def test_register_namelast():
    # no last name
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', 'valid', '')
    # last name more than 50 characters   
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', 'valid', '012345678901234567890123456789012345678901234567890')
        
def test_login_invalid_email():
    # login with non-existing user
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    with pytest.raises(InputError) as e:
        auth.auth_login('diffemail@gmail.com', 'valid123')
    
    # login with existing user
    auth.auth_login('validemail@gmail.com', 'valid123')
    
def test_login_invalid_password():
    # incorrect password
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    with pytest.raises(InputError) as e:
        auth.auth_login('validemail@gmail.com', 'diffpass')
    
def test_logout_success():
    # logout user that's logged in
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    token = auth.auth_login('validemail@gmail.com', 'valid123')
    temp = auth.auth_logout(token['token'])
    
    assert temp['is_success'] == True
    
    #logout bad token
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    auth.auth_logout('nonexistingtoken') == False

def test_data_changes():
    # elements stored correctly
    clear()
    auth.auth_register('philsmart@gmail.com', 'bigboys111', 'Phil', 'Smart')
    
    assert users[0]['u_id'] == 1
    assert users[0]['email'] == 'philsmart@gmail.com'
    assert users[0]['password'] == 'bigboys111'
    assert users[0]['name_first'] == 'Phil'
    assert users[0]['name_last'] == 'Smart'
    assert users[0]['channels'] == []
    assert users[0]['token'] == '1'
    assert users[0]['handle'] == 'philsmart'
    
    auth.auth_register('darryngarryn@gmail.com', 'niceice123', 'Darryn', 'Garryn')
    
    assert users[1]['u_id'] == 2
    assert users[1]['email'] == 'darryngarryn@gmail.com'
    assert users[1]['password'] == 'niceice123'
    assert users[1]['name_first'] == 'Darryn'
    assert users[1]['name_last'] == 'Garryn'
    assert users[1]['channels'] == []
    assert users[1]['token'] == '2'
    assert users[1]['handle'] == 'darryngarryn'
    
    # u_id created in ascending order
    auth.auth_register('userid3@gmail.com', 'valid123', 'valid', 'valid')
    auth.auth_register('userid4@gmail.com', 'valid123', 'valid', 'valid')
    auth.auth_register('userid5@gmail.com', 'valid123', 'valid', 'valid')
    auth.auth_register('userid6@gmail.com', 'valid123', 'valid', 'valid')
    
    assert users[2]['u_id'] == 3
    assert users[3]['u_id'] == 4
    assert users[4]['u_id'] == 5
    assert users[5]['u_id'] == 6
    
    # handle cut off above 20 characters
    
    auth.auth_register('bighandle@gmail.com', 'valid123', 'Yothisisgonna', 'Bemassive')
    
    assert users[6]['handle'] == 'yothisisgonnabemassi'
     
    # duplicate handles
    auth.auth_register('twohandles@gmail.com', 'valid123', 'Name', 'Name')
    auth.auth_register('twohandles1@gmail.com', 'valid123', 'Name', 'Name')
    
    assert users[7]['handle'] == 'namename'
    assert users[8]['handle'] == '9namename'
    
    # duplicate with big handle
    
    auth.auth_register('bighandle2@gmail.com', 'valid123', 'Yothisisgonna', 'Bemassive')
    
    assert users[9]['handle'] == '10yothisisgonnabemas'
    
    
    
    
     
    
    
    
        
    
    
    
    
