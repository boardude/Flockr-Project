## General
1. we assume that the very first user who signs up is the owner of flockr(user[0]).
2. we assume that all data will be stored in data.py file in iteration 1, and every single file imports data.py if it need.
3. we assume that we do not cover data storing persistence in iteration 1.

## auth
1. we assume that token == str(u_id) for iteration 1.
2. we assume that auth_login and auth_register will not generate a unique token.
3. we assume that users can always log out in iteration 1 because we cannot test token validity.
4. we assume that user will always enter valid name_first and name_last (no numbers and symbols).

## channel
1. we assume that program will also raise access error if the token cannot refer to a valid user.
2. we assume that program will keep the channel if all members of it leave that channel.
3. we assume that there is no bug in channel_messages for iteration 1 because we need message_send() to test it.
4. we assume that if authorised user invites a uses who is already a member of channel, 
                    program will ignore the request and return directly.
5. we assume that if a user tries to join a channel he is already in, program will ignore the request and return directly.
6. we assume that if the owner of flockr enter any channel, channel will set this user as owner of channel directly.
7. we assume that the owner of channel cannot modify channel owner permission of the owner of flockr.
8. we assume that the owner of channel can modify other owner's permission whatever he is the channel creater
9. we assume that only after the owner of flockr enters a channel, he will have owner permission of that channel

## channels
**Validity of tokens as parameters for channels_\* functions**  
Assume only valid tokens (users that are registered + logged in) will be given to these functions, and that channels_* functions do not need to check for invalid tokens as InputError exceptions.

**Token taken as is for channels_\* functions**  
Following from the above assumption, the token input will be taken as is in all channels_* functions. This means that the given token will be assumed valid regardless of its characteristics such as data type. This includes the case where an empty token is given.

**Duplicate channel details for channels_create()**  
Assume a new channel with the same details (token, name, is_public) as an existing channel will be created regardless since the channel_id differs the two.


