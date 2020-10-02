from data import users, channels
### temporary file only for channel_test
def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create(token, name, is_public):
    new_channel = {}
    user = token_to_user(token)
    new_channel['channel_id'] = len(channels) + 1
    new_channel['public'] = is_public
    new_channel['name'] = name
    new_channel['owner_members'] = [user['u_id']]
    new_channel['all_members'] = [user['u_id']]
    new_channel['messages'] = []
    channels.append(new_channel)
    user['channels'].append(new_channel['channel_id'])
    return {
        'channel_id': new_channel['channel_id'],
    }

### help function

def token_to_user(token):
    for user in users:
        if user['token'] == token:
            return user
   # return False


