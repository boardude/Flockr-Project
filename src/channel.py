from data import users, channels
from error import InputError, AccessError

'''
    5 help functions:
        1. token_to_user(token)
            this will take a given token and return a user(dict)
            if there is no such a user with that token, it will return False
        2. uid_to_user(u_id)
            this will take a given u_id and return a user(dict)
            if there is no such a user with that token, it will return False
        3. uid_to_member(u_id)
            this will take a given u_id and return a member(dict) for chennel_details()
        4. channelId_to_channel(channel_id)
            this will take a given channel_id and return a channel(dict)
        5. is_user_in_channel(token, channel_id)
            this will check whether the user is in the channel
'''

def channel_invite(token, channel_id, u_id):
    invited_user = uid_to_user(u_id)
    channel = channelId_to_channel(channel_id)
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
    channel = channelId_to_channel(channel_id)
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
    channel = channelId_to_channel(channel_id)
    # input error when Channel ID is not a valid channel
    if channel is False:
        raise InputError()

    # input error when start is greater than the total number 
    # of messages in the channel
    if start >= len(channel['messages']):
        raise InputError()

    # access error when Authorised user is not a member of channel with channel_id
    if is_user_in_channel(token, channel_id) == False:
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
    channel = channelId_to_channel(channel_id)
    user = token_to_user(token)
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
    user = token_to_user(token)
    channel = channelId_to_channel(channel_id)
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
    inviter = token_to_user(token)
    channel = channelId_to_channel(channel_id)
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
    if inviter is False:
        raise AccessError()
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
    remover = token_to_user(token)
    channel = channelId_to_channel(channel_id)
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
    if remover is False:
        raise AccessError()
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

### convert token to a user(dict)
### return user if token is valid 
###     else return false if it is invalid
def token_to_user(token):
    for user in users:
        if user['token'] == token:
            return user
    return False

### convert u_id to a user(dict)
### return user if token is valid 
###     else return false if it is invalid
def uid_to_user(u_id):
    for user in users:
        if user['u_id'] == u_id:
            return user
    return False

### create a new channel member(dict)
def uid_to_member(u_id):
    user = uid_to_user(u_id)
    return {
        'u_id' : user['u_id'],
        'name_first' : user['name_first'],
        'name_last' : user['name_last']
    }

### convert channel_id to channel(dict)
### return channel if id is valid
###     else return false if it is invalid
def channelId_to_channel(channel_id):
    for channel in channels:
        if channel['channel_id'] == channel_id:
            return channel
    return False

### check a user is a member or not
def is_user_in_channel(token, channel_id):
    user = token_to_user(token)
    if user == False:
        return False
    for channel in user['channels']:
        if channel == channel_id:
            return True
    return False
