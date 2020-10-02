from data import users, channels
from error import InputError

"""
HELPER FUNCTIONS
    1. is_channel_name_valid(name): checks if channel name more than 20 characters,
    in which case it is invalid
"""

########### GLOBAL VARIABLES ###############
# total number of channels created at any given time
# is the channel_id of a newly created channel
channels_created = 0

#### INTERFACE FUNCTION IMPLEMENTATIONS ####
def channels_list(token):
    """channels_user = []
    for channel in channels:
        if token is in channel['all_members']:
            channels_user.append(channel) """

    for user in users:
        if user['u_id'] is token:
            return user['channels']
    
    return []   # user not found

def channels_listall(token):
    return channels

def channels_create(token, name, is_public):
    # check name validity
    if is_name_valid(name) is False:
        raise InputError()

    # create new channel
    new_channel = {}
    new_channel['channel_id'] = channels_total 
    new_channel['public'] = is_public
    new_channel['name'] = name
    new_channel['owner_members'] = [token]
    new_channel['all_members'] = [token]
    new_channel['messages'] = []
    
    # add new channel to channels list in data.py
    channels.append(new_channel)

    # add new channel to user's channels list
    for user in users:
        if user['u_id'] is token:
            user['channels'].append(new_channel)

    # increment total number of channels created
    global channels_total
    channels_total += 1

    # return channel_id    
    return {
        'channel_id': new_channel['channel_id'],
    }


############### HELPER FUNCTIONS #################
# check if name is invalid (more than 20 characters)
# returns False if invalid, otherwise True
def is_name_valid(name):
    if len(name) > 20:
        return False
    else:
        return True