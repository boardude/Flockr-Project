# Yicheng (Mike) Zhu
# Last updated 4/10/2020

from data import users, channels, create_new_channel
from error import InputError

"""
HELPER FUNCTIONS
    1. is_channel_name_valid(name): checks if channel name more than 20 characters,
    in which case it is invalid
    2. get_uid_from_token(token): returns corresponding u_id given a token
"""

########### GLOBAL VARIABLES ###############
# total number of channels created at any given time
# is the channel_id of a newly created channel
channels_created = 1

#### INTERFACE FUNCTION IMPLEMENTATIONS ####
def channels_list(token):
    for user in users:
        if user['token'] is token:
            user_channel_ids = user['channels']
            break

    user_channels = []
    
    for user_channel_id in user_channel_ids:
        for channel in channels:
            if channel['channel_id'] == user_channel_id:
                new_channel_entry = {}
                new_channel_entry['channel_id'] = channel['channel_id']
                new_channel_entry['name'] = channel['name']
                user_channels.append(new_channel_entry)
    
    return {
        'channels': user_channels,
    }

def channels_listall(token):
    all_channels = []
    for channel in channels:
        new_channel_entry = {}
        new_channel_entry['channel_id'] = channel['channel_id']
        new_channel_entry['name'] = channel['name']
        all_channels.append(new_channel_entry)

    return {
        'channels': all_channels,
    }

def channels_create(token, name, is_public):
    global channels_created

    # check name validity
    if is_name_valid(name) is False:
        raise InputError()

    # create new channel
    new_user_id = get_uid_from_token(token)
    new_channel = create_new_channel(channels_created, is_public, name, new_user_id)
    
    # add new channel to channels list in data.py
    channels.append(new_channel)

    # add new channel_id to user's channels list
    for user in users:
        if user['token'] is token:
            user['channels'].append(new_channel['channel_id'])

    # increment total number of channels created
    channels_created += 1

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

# returns corresponding u_id given a token
def get_uid_from_token(token):
    for user in users:
        if user['token'] == token:
            return user['u_id']