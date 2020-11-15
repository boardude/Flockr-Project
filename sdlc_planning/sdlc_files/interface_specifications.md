# **Interface Specifications** #

|Function name|HTTP Method|Parameters|Return type|Exceptions|Description|
|-------------|-----------|----------|-----------|----------|-----------|
|channels/ groupcreate|POST|```{token, name}```|```{group_id}```|**InputError** when any of: </br> <ul><li> Name is more than 20 characters long|Creates a new channel group with that name.|
|channel/ groupaddchannel|PUT|```{token, group_id, channel_id}```|```{}```|**InputError** when any of: </br> <ul><li> Group does not exist</li><li> Channel with channel_id does not exist</ul> **AccessError** when any of: </br> <ul><li> User is not the creator of the group|Given a channel by its ```channel_id```, adds it to the channel group with ```group_id```.|
|direct/create|POST|```{token, u_id}```|```{dm_id}```|**InputError** when any of: </br> <ul><li> ```u_id``` does not refer to a valid user</li><li>```u_id``` refers to self (```token```)</li><li> A direct message chat already exists with that user|Given a user specified by ```u_id```, creates a direct message chat with the user.|
|direct/send|POST|```{token, dm_id, message}```|```{message_id}```|**InputError** when any of: </br><ul><li> Message is more than 1000 characters </li><li>```dm_id``` does not refer to a valid direct message chat</ul> **AccessError** when any of: <ul><li> The authorised user is not part of the direct message chat|Send a message from authorised to the direct message chat specified by ```dm_id```|
|direct/sendlater|POST|```{token, dm_id, message, time_sent}```|```{message_id}```|**InputError** when any of: <br><ul><li> Message is more than 1000 characters<li>```dm_id``` does not refer to a valid direct message chat<li>Time sent is a time in the past</ul>**AccessError** when any of: <ul><li> The authorised user is not part of the direct message chat|Send a message from authorised user to the direct message chat specified by ```dm_id``` automatically at a specified time in the future|
|file/send|POST|```{token, channel_id, path}```|```{file_id}```|**InputError** when any of:<br><ul><li> ```channel_id``` does not refer to a valid channel <li> ```path``` does not refer to a valid file <li> File is larger than 100 MB</ul> **AccessError** when any of: <br><ul><li> The authorised user has not joined the channel they are trying to send the file to|Send a file from authorised_user to the channel specified by channel_id|
|file/senddirect|POST|   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |