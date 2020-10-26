## General
1. We assume that the very first user who signs up is the owner of flockr(user[0]).
2. We assume that all data will be stored in data.py, and every single file imports data.py if it need.
3. We assume that we do not cover data storing persistence in iteration 2.
4. We assume that the key for encoding token is a variable called SECRET with value 'grape6'.
5. We assume that a given token is invalid if it cannot be decoded or its digital signature shows user has logged out except auth_logout.
6. We assume that an invalid token would raise an accesserror except auth_login and auth_logout.

## auth
1. We assume that token is not equal to str(u_id) for iteration 2 and would be encoded by jwt.
2. We assume that auth_login and auth_register will generate a same token to show the user has login.
3. We assume that it would raise an error if a logout user's token is passed into auth_logout.
4. We assume that user will always enter valid name_first and name_last (no numbers).
5. We assume that it will not raise an error if a user login twice.
6. We assume that entered password would be encoded by hashlib.sha256 which cannot be reverted.
7. We assume that it will return false if given token refers to a user with logout status.
8. We assume that it will login automatically after a user registers.

## channel
1. We assume that an owner of flockr will not be set as an owner of channel after he enters a channel. But the user still has permission of channel owner.
2. We assume that program will keep the channel if all members of it leave that channel.
3. We assume that an owner of channel can modify other owner's permission no matter he is the creator or not.
4. We assume that program will not raise an error if start is equal to the number of messages in the channel in channel_messages
5. We assume that if authorised user invites a uses who is already a member of channel, program will ignore the request and return directly.
6. We assume that if a user tries to join a channel he is already in, program will ignore the request and return directly.
7. We assume that only after the owner of flockr enters a channel, he will have owner permission of that channel.

## channels
**Validity of tokens as parameters for channels_\* functions**  
Assume only valid tokens (users that are registered + logged in) will be given to these functions, and that channels_* functions do not need to check for invalid tokens as InputError exceptions.

**Token taken as is for channels_\* functions**  
Following from the above assumption, the token input will be taken as is in all channels_* functions. This means that the given token will be assumed valid regardless of its characteristics such as data type. This includes the case where an empty token is given.

**Duplicate channel details for channels_create()**  
Assume a new channel with the same details (token, name, is_public) as an existing channel will be created regardless since the channel_id differs the two.

## message
1. We assume that all messages will have a unique message_id which is equal to 10000 * channel_id + the sequence was sent.
2. We assume that users can send an empty string in message_send.
3. We assume that it will raise an access error when given channel_id is invalid.
4. We assume that all messages will keep its unique message_id after any message is removed.
5. We assume that the length of message can be greater than 1000 in message_edit.
6. We assume that message_id would be always valid in message_edit except when new message is an empty string.

## user
1. We assume that name cannot be empty in user_setname.
2. We assume that it will raise an error when a user tries to set his email with his current email.
3. We assume that it will raise an error when a user tries to set his handle with his current handle.

## other
1. We assume that search will return all messages containing given query_str.
2. We assume that an owner of flockr can modify other owner's permission no matter he is the first registerd user or not. 
