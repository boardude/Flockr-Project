import auth
from other import clear
from error import InputError
import pytest

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
        all:
            1. logout fails
            2. login fails
            3. register, login succeeds
            4. register, logout fails
            5. register, login, logout succeeds
'''

def test_register_email():
    
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

    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
        
def test_register_password():
    
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'inval', 'valid', 'valid')
    
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '', 'valid', 'valid')
    
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    
def test_register_namefirst():
    
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', '', 'valid')
        
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', '012345678901234567890123456789012345678901234567890', 'valid')
        
def test_register_namelast():
    
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', 'valid', '')
        
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'valid123', 'valid', '012345678901234567890123456789012345678901234567890')
        
def test_login_invalid_email():
    
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    with pytest.raises(InputError) as e:
        auth.auth_login('diffemail@gmail.com', 'valid123')
    
    auth.auth_login('validemail@gmail.com', 'valid123')
    
def test_login_invalid_password():
    
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    with pytest.raises(InputError) as e:
        auth.auth_login('validemail@gmail.com', 'diffpass')
    
def test_logout_success():
    
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    auth.auth_logout('validemail@gmail.com') == True
    
    clear()
    auth.auth_register('validemail@gmail.com', 'valid123', 'valid', 'valid')
    auth.auth_logout('nonexistingtoken') == False
    
    
    
    
    
    
        
    
    
    
    
