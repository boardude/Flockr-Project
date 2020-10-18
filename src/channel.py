'''
import data.py for data storing
import error.py for error raising
'''
from error import InputError, AccessError
from data import users, channels

def channel_invite(token, channel_id, u_id):
    '''
    This will invite a user (with user id u_id) to join a channel with channel_id.
    Once invited the user is added to the channel immediately.

    Args:
        param1: invitor's token.
        param2: target channel.
        param3: invited user's u_id

    Returns:
        This will return an empty dictionary.

    Raises:
        InputError:
            1. channel_id does not refer to a valid channel.
            2. u_id does not refer to a valid user.
        AccessError:
            1. the authorised user is not already a member of the channel.
            2. given token does not refer to a valid token
    '''
    invited_user = uid_to_user(u_id)
    channel = channelid_to_channel(channel_id)
    # input error when u_id does not refer to a valid user
    if invited_user is False:
        raise InputError()

    # input error when channel_id does not refer to a valid channel.
    if channel is False:
        raise InputError()

    # accesss error when the authorised user is not already a member of the channel
    if is_user_in_channel(token, channel_id) is False:
        raise AccessError()

    # already in channel
    if is_user_in_channel(invited_user['token'], channel_id):
        return {
        }

    channel['all_members'].append(invited_user['u_id'])
    invited_user['channels'].append(channel_id)
    # if u_id refers to the owner of flockr
    if invited_user['u_id'] == users[0]['u_id']:
        channel['owner_members'].append(invited_user['u_id'])
    return {
    }

def channel_details(token, channel_id):
    '''
    This will provide basic details about a channel whose Channel Id is channel_id.
    Also, the authorised user is part of that channel.

    Args:
        param1: authorised user's token.
        param2: target channel.

    Returns:
        This will return a dictionary with channel details.
        {
            'name': channel['name'],
            'owner_members': owner_details,
            'all_members': all_details,
        }

    Raises:
        InputError:
            1. channel_id does not refer to a valid channel.
            2. u_id does not refer to a valid user.
        AccessError:
            1. the authorised user is not already a member of the channel.
            2. given token does not refer to a valid token
    '''
    channel = channelid_to_channel(channel_id)
    # inputerror when Channel ID is not a valid channel
    if channel is False:
        raise InputError()

    # access error when Authorised user is not
    # a member of channel with channel_id
    if is_user_in_channel(token, channel_id) is False:
        raise AccessError()

    owner_details = []
    all_details = []
    for owner in channel['owner_members']:
        owner_details.append(uid_to_member(owner))
    for member in channel['all_members']:
        all_details.append(uid_to_member(member))
    return {
        'name': channel['name'],
        'owner_members': owner_details,
        'all_members': all_details,
    }

def channel_messages(token, channel_id, start):
    '''
    This will return a list of messages from [start] of
    channel with channel_id. It contains up to 50 messages between
    index "start" and "start + 50". Message with index 0 is the most
    recent message in the channel. This function returns a new index "end"
    which is the value of "start + 50", or, if this function has returned
    the least recent messages in the channel, returns -1 in "end" to indicate
    there are no more messages to load after this return.

    Args:
        param1: authorised user's token.
        param2: target channel.
        param3: start index of messages

    Returns:
        This will return a dictionary with channel details.
        {
            'messages' : (a list of messages),
            'start' : (start index),
            'end' : (end index),
        }

    Raises:
        InputError:
            1. channel_id does not refer to a valid channel.
            2. start is greater than the total number of messages in the channel.
        AccessError:
            1. Authorised user is not a member of channel with channel_id.
            2. given token does not refer to a valid token
    '''
    channel = channelid_to_channel(channel_id)
    # input error when Channel ID is not a valid channel
    if channel is False:
        raise InputError()

    # input error when start is greater than the total number
    # of messages in the channel
    if start >= len(channel['messages']):
        raise InputError()

    # access error when Authorised user is not a member of channel with channel_id
    if is_user_in_channel(token, channel_id) is False:
        raise AccessError()

    return_messages = []
    end = start + 50
    if end >= len(channel['messages']):
        end = -1
        for message in channel['messages'][start:]:
            return_messages.append(message)
    else:
        for message in channel['messages'][start:start + 49]:
            return_messages.append(message)
    return {
        'messages' : return_messages,
        'start' : start,
        'end' : end,
    }

def channel_leave(token, channel_id):
    '''
    This will remove authorised user from given channel.
    If the last user of that channel leaves, we will keep that channel in data.

    Args:
        param1: authorised user's token.
        param2: target channel.

    Returns:
        This will return an empty dictionary.

    Raises:
        InputError:
            Channel ID is not a valid channel
        AccessError:
            1. Authorised user is not a member of channel with channel_id
            2. given token does not refer to a valid token
    '''
    user = token_to_user(token)
    # access error when the token does not refer to a valid token
    if user is False:
        raise AccessError()

    channel = channelid_to_channel(channel_id)
    # input error when Channel ID is not a valid channel
    if channel is False:
        raise InputError()

    # access error when Authorised user is not
    # a member of channel with channel_id
    if is_user_in_channel(token, channel_id) is False:
        raise AccessError()

    user['channels'].remove(channel_id)
    channel['all_members'].remove(user['u_id'])
    for owner in channel['owner_members']:
        if owner == user['u_id']:
            channel['owner_members'].remove(user['u_id'])
    return {
    }

def channel_join(token, channel_id):
    '''
    This will add authorised user to given channel. If user is the
    owner of flockr, it will set user as onwer of that channel.

    Args:
        param1: authorised user's token.
        param2: target channel.

    Returns:
        This will return an empty dictionary.

    Raises:
        InputError:
            Channel ID is not a valid channel
        AccessError:
            1. channel_id refers to a channel that is private
                (when the authorised user is not a global owner)
            2. given token does not refer to a valid token
    '''
    user = token_to_user(token)
    # access error when the token does not refer to a valid token
    if user is False:
        raise AccessError()

    channel = channelid_to_channel(channel_id)
    # input error when Channel ID is not a valid channel
    if channel is False:
        raise InputError()

    # access error when channel_id refers to a channel that is private
    # the authorised user is not a global owner
    if channel['public'] is False and user is not users[0]:
        raise AccessError()

    # already in the channel
    if is_user_in_channel(token, channel_id) is True:
        return {
        }

    channel['all_members'].append(user['u_id'])
    user['channels'].append(channel_id)
    # owner of flockr will become the owner of channel
    if user['u_id'] == users[0]['u_id']:
        channel['owner_members'].append(user['u_id'])
    return {
    }

def channel_addowner(token, channel_id, u_id):
    '''
    This will set the user with u_id as the owner of target channel.
    Token refers to one of the owner of target channel.
    It will return an empty dictionaty.

    Args:
        param1: authorised user's token.
        param2: target channel.
        param3: new owner's u_id

    Returns:
        This will return an empty dictionary.

    Raises:
        InputError:
            1. Channel ID is not a valid channel
            2. When user with user id u_id is already an owner of the channel
        AccessError:
            1. when the authorised user is not an owner of
                the flockr, or an owner of this channel
            2. given token does not refer to a valid token
    '''
    inviter = token_to_user(token)
    # access error when the token does not refer to a valid token
    if inviter is False:
        raise AccessError()

    channel = channelid_to_channel(channel_id)
    # input error when Channel ID is not a valid channel
    if channel is False:
        raise InputError()

    # input error when When user with user id u_id
    # is already an owner of the channel
    for owner in channel['owner_members']:
        if owner == u_id:
            raise InputError()

    # access error when the authorised user is not
    # an owner of the flockr, or an owner of this channel
    permitted = False
    for owner in channel['owner_members']:
        if owner == inviter['u_id']:
            permitted = True
            break
    if permitted is not True:
        raise AccessError()

    channel['owner_members'].append(u_id)
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    '''
    This will remove the user with u_id from the owners of target channel.
    If u_id refers to the owner of flockr, it will ignore the request.
    Token refers to one of the owner of target channel.
    It will return an empty dictionaty.

    Args:
        param1: authorised user's token.
        param2: target channel.
        param3: the user's u_id who is removed from owners

    Returns:
        This will return an empty dictionary.

    Raises:
        InputError:
            1. Channel ID is not a valid channel
            2. When user with user id u_id is not an owner of the channel
        AccessError:
            1. when the authorised user is not an owner of
                the flockr, or an owner of this channel
            2. given token does not refer to a valid token
    '''
    remover = token_to_user(token)
    # access error when the token does not refer to a valid token
    if remover is False:
        raise AccessError()

    channel = channelid_to_channel(channel_id)
    # input error when Channel ID is not a valid channel
    if channel is False:
        raise InputError()

    # input error when user with user id u_id is not
    # an owner of the channel
    is_owner = False
    for owner in channel['owner_members']:
        if owner == u_id:
            is_owner = True
            break
    if is_owner is False:
        raise InputError()

    # accesss error when the authorised user is not
    # an owner of the flockr, or an owner of this channel
    permitted = False
    for owner in channel['owner_members']:
        if owner == remover['u_id']:
            permitted = True
            break
    if permitted is not True:
        raise AccessError()

    if u_id != users[0]['u_id']:
        channel['owner_members'].remove(u_id)
    return {
    }

########## help functions ##########

def token_to_user(token):
    '''
    This is a simple helper function.
    It will return a user with given token if it exists in data,
    else return False

    Args:
        param1: token

    Returns:
        This will return uesr(dictionary) if token refers to a valid user in data,
        else return False.

    Raises:
        this will not raise any error
    '''
    for user in users:
        if user['token'] == token:
            return user
    return False

def uid_to_user(u_id):
    '''
    This is a simple helper function.
    It will return a user with given u_id if it exists in data,
    else return False

    Args:
        param1: u_id

    Returns:
        This will return uesr(dictionary) if u_id refers to a valid user in data,
        else return False.

    Raises:
        this will not raise any error
    '''
    for user in users:
        if user['u_id'] == u_id:
            return user
    return False

def uid_to_member(u_id):
    '''
    This is a simple helper function.
    It will return a member type data with given u_id if it exists in data,
    else return False

    Args:
        param1: u_id

    Returns:
        This will return member(dictionary) if u_id refers to a valid user in data,
        else return False.

    Raises:
        this will not raise any error
    '''
    user = uid_to_user(u_id)
    return {
        'u_id' : user['u_id'],
        'name_first' : user['name_first'],
        'name_last' : user['name_last']
    }

def channelid_to_channel(channel_id):
    '''
    This is a simple helper function.
    It will return a channel with given channel_id if it exists in data,
    else return False

    Args:
        param1: channel_id

    Returns:
        This will return channel(dictionary) if token refers to a valid chanenl in data,
        else return False.

    Raises:
        this will not raise any error
    '''
    for channel in channels:
        if channel['channel_id'] == channel_id:
            return channel
    return False

def is_user_in_channel(token, channel_id):
    '''
    This is a simple helper function.
    It will test whether a user with given token is in target channel.

    Args:
        param1: token

    Returns:
        This will return a boolean value.
        It will return True if the user is in target channel.
        else return False.

    Raises:
        this will not raise any error
    '''
    user = token_to_user(token)
    if user is False:
        return False
    for channel in user['channels']:
        if channel == channel_id:
            return True
    return False
