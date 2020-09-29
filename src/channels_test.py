from channels import channels_list, channels_listall, channels_create
from other import clear
from error import InputError

def test_list():
    clear()
    temp = channels_list('TdsfGWL')
    assert isinstance(temp['channels'], list) is True

def test_listall():
    clear()
    temp = channels_listall('TdsfGWL')
    assert isinstance(temp['channels'], list) is True

def test_create():

    clear()
    with pytest.raises(InputError) as e:
        channels_create('TskWlGS', 'Channel NameThatHasMoreThanTwentyCharacters', True) # long character name exception 

    clear()
    temp = channels_create('SDLlvSd', 'Channel 0', True)      # is_public test 0
    assert temp['channel_id'] == 0

    clear()
    temp = channels_create('SDfGlwf', 'Channel 1', False) 
    assert temp['channel_id'] == 1                            # is_public test 1

    clear()
    temp = channels_create('', 'Channel 2', True)             # empty parameter
    assert temp['channel_id'] == 2

    clear()
    temp = channels_create('ESGsdwf', 'Channel 3', False)     # empty parameter
    assert temp['channel_id'] == 3

    clear()
    temp = channels_create('wfDDFSF', 'Channel 4', True)
    assert temp['channel_id'] == 4                            # empty parameters