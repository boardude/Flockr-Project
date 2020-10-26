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
from helper import get_user_from_token, get_channel_from_id

#### INTERFACE FUNCTION IMPLEMENTATIONS ####
def channels_list(token):
    """
        Returns a list of all channels (with channel name & channel id)
        that the authorised user is part of when given the user's token
    """
    # check token validity
    auth_user = get_user_from_token(token)
    if auth_user is None:
        raise AccessError(description="Unauthorised access")
    # get list of channel_id
    user_channels = auth_user['channels']
    return {
        'channels': list(map(channel_detail, user_channels)),
    }

def channels_listall(token):
    """
        Returns a list of all channels (with channel name & channel id) when
        given the token of any authenticated user
    """

    # check token validity
    auth_user = get_user_from_token(token)
    if auth_user is None:
        raise AccessError(description="Unauthorised access")
    # get list of channel_id
    all_channels = []
    for channel in channels:
        all_channels.append(channel['channel_id'])
    return {
        'channels': list(map(channel_detail, all_channels)),
    }

def channels_create(token, name, is_public):
    """
        Creates a new channel with that when given the token of an authorised user, the
        new channel's name, and its is_public property. Channel ID of new channel is returned.
    """

    user = get_user_from_token(token)
    # check name validity
    if len(name) > 20:
        raise InputError(description="Name cannot be longer than 20 characters")

    # check token validity
    if user is None:
        raise AccessError(description="Unauthorised access")

    # create new channel in data.py
    new_channel = create_new_channel(len(channels) + 1, is_public, name, user['u_id'])

    # add new channel_id to user's channels list
    user['channels'].append(new_channel['channel_id'])

    # return channel_id
    return {
        'channel_id': new_channel['channel_id'],
    }

def channel_detail(channel_id):
    '''
    a helper function to tranfer channel_id to associated info
    '''
    channel = get_channel_from_id(channel_id)
    return {
        'channel_id' : channel['channel_id'],
        'name' : channel['name'],
    }
