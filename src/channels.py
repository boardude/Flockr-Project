# Yicheng (Mike) Zhu
# Last updated 4/10/2020

"""
    data module contains users and channels list structures to store data
    and helper functions for creating a new user and a new channel

    error module contains custom exceptions, including InputError
    and AccessError
"""
from data import users, channels, create_new_channel
from error import InputError

########### GLOBAL VARIABLES ###############
# total number of channels created at any given time
# is the channel_id of a newly created channel
channels_created = 1

#### INTERFACE FUNCTION IMPLEMENTATIONS ####
def channels_list(token):
    """
        Returns a list of all channels (with channel name & channel id)
        that the authorised user is part of when given the user's token
    """

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
    """
        Returns a list of all channels (with channel name & channel id) when
        given the token of any authenticated user
    """

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
    """
        Creates a new channel with that when given the token of an authorised user, the
        new channel's name, and its is_public property. Channel ID of new channel is returned.
    """

    global channels_created

    # check name validity
    if is_name_valid(name) is False:
        raise InputError()

    # create new channel in data.py
    new_user_id = get_uid_from_token(token)
    new_channel = create_new_channel(channels_created, is_public, name, new_user_id)

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
def is_name_valid(name):
    """
        Check if name is valid (less than 20 characters), returning True if valid,
        otherwise False
    """
    if len(name) > 20:
        return False

    return True

def get_uid_from_token(token):
    """
        Return the corresponding u_id when given the token of an authorised
        user
    """
    for user in users:
        if user['token'] == token:
            return user['u_id']

    return None
