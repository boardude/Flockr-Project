### General


### auth



### channel


### channels
**Validity of tokens as parameters for channels_\* functions**
Assume only valid tokens (users that are registered + logged in) will be given to these functions, 
and that channels_* functions do not need to check for invalid tokens as InputError exceptions

**Token taken as is for channels_\* functions**
Following from the above assumption, the token input will be taken as is in all channels_* functions. 
This means that the given token will be assumed valid regardless of its characteristics such as data type.
This includes the case where an empty token is given.

**Duplicate channel details for channels_create()**
Assume a new channel with the same details (token, name, is_public) as an existing channel will be 
created regardless since the channel_id differs the two


