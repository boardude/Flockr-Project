''' Test file for message.py '''

import pytest
import auth
from other import clear
from error import InputError, AccessError
import message
from data import channels
from channels import channels_create
import channel

channels_create(1, 'Channel 1', True)
msg_dict = channels[0].get('messages')

def test_msg_send():
    '''test for message_send'''
    #returns message_id
    auth.auth_register("validemail@gmail.com", 'V@l1dPa55w0rd', 'Hayden', 'Smith')
    channel.channel_join(1, 1)

    assert message.message_send(1, 1, '1st message') == {'message_id': 1}
    assert message.message_send(1, 1, '2nd message') == {'message_id': 2}

    #data stored correctly
    message.message_send(1, 1, '1st message')
    message.message_send(1, 1, '2nd message')

    assert msg_dict.get('message') == ['1st message', '2nd message']

    #inputError when message > 1000 characters
    with pytest.raises(InputError):
        message.message_send(1, 1, 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Na')

    #accessError when the authorised user has not joined the channel they
    #are trying to post to
    with pytest.raises(AccessError):
        message.message_send(1, 1, 'This should fail!')

def test_msg_remove():
    '''test for message_remove'''
    clear()
    #removes message from data
    auth.auth_register("validemail@gmail.com", 'V@l1dPa55w0rd', 'Hayden', 'Smith')
    channel.channel_join(1, 1)

    message.message_send(1, 1, 'I will delete this message!')
    message.message_remove(1, 1)

    assert msg_dict == []

    #InputError when message (based on ID) no longer exists
    with pytest.raises(InputError):
        message.message_remove(1, 1)

    #AccessError when message not sent by user making the request
    message.message_send(1, 1, 'This message is by user 1')
    auth.auth_logout(1)
    auth.auth_register("validEmail@gmail.com", 'V@l1dPa55w0rd', 'User', '2')

    with pytest.raises(AccessError):
        message.message_remove(2, 1)

    #AccessError when user is not an owner of the channel
    message.message_send(2, 1, 'Ill try to delete this')

    with pytest.raises(AccessError):
        message.message_remove(2, 2)

def test_msg_edit():
    '''test for message_edit'''
    clear()
    #message updated with new text
    auth.auth_register("validemail@gmail.com", 'V@l1dPa55w0rd', 'Hayden', 'Smith')
    channel.channel_join(1, 1)

    message.message_send(1, 1, 'This message is not edited')
    message.message_edit(1, 1, 'This message is edited')

    assert msg_dict.get('message') == ['This message is edited']

    #delete message if new message is an empty string
    message.message_edit(1, 1, '')
    assert msg_dict.get('message') == []

    #AccessError when message not sent by user
    message.message_send(1, 1, 'User 1 sent this!')
    auth.auth_logout(1)
    auth.auth_register("validEmail@gmail.com", 'V@l1dPa55w0rd', 'User', '2')
    channel.channel_join(2, 1)
    channel.channel_addowner(2, 1, 2)

    with pytest.raises(AccessError):
        message.message_edit(2, 1, 'This isnt changed by user 2!')

    #AccessError when user is not an owner of the channel
    message.message_send(2, 1, 'This is a message')

    channel.channel_removeowner(2, 1, 2)

    with pytest.raises(AccessError):
        message.message_edit(2, 1, 'This cant be edited!')
