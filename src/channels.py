# Yicheng (Mike) Zhu
# Last updated 20/10/2020

"""
    data module contains users and channels list structures to store data
    and helper functions for creating a new user and a new channel

    error module contains custom exceptions, including InputError
    and AccessError
"""
from data import users, channels, create_new_channel
from error import InputError, AccessError
from helper import is_token_valid, get_uid_from_token

#### INTERFACE FUNCTION IMPLEMENTATIONS ####
def channels_list(token):
    """
        Returns a list of all channels (with channel name & channel id)
        that the authorised user is part of when given the user's token
    """

    # check token validity
    if not is_token_valid(token):
        raise AccessError

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

    # check token validity
    if not is_token_valid(token):
        raise AccessError

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

    # check name validity
    if not is_name_valid(name):
        raise InputError()

    # check token validity
    if not is_token_valid(token):
        raise AccessError

    # create new channel in data.py
    new_user_id = get_uid_from_token(token)
    new_channel = create_new_channel(len(channels), is_public, name, new_user_id)

    # add new channel_id to user's channels list
    for user in users:
        if user['token'] is token:
            user['channels'].append(new_channel['channel_id'])

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
