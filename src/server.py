import sys
from auth import auth_login, auth_logout, auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave
from channel import channel_join, channel_addowner, channel_removeowner
from channels import channels_create, channels_list, channels_listall
from message import message_send, message_remove, message_edit
from user import user_profile, user_profile_setemail, user_profile_sethandle, user_profile_setname
from other import clear, users_all, search, admin_userpermission_change
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

########################################
############## auth.py #################
########################################
@APP.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    return dumps(auth_login(email, password))

@APP.route('/auth/logout', methods=['POST'])
def logout():
    token = request.get_json()['token']
    return dumps(auth_logout(token))

@APP.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    return dumps(auth_register(email, password, name_first, name_last))

########################################
############# channel.py ###############
########################################
@APP.route('/channel/invite', methods=['POST'])
def invite():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])
    return dumps(channel_invite(token, channel_id, u_id))

@APP.route('/channel/details', methods=['GET'])
def get_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(channel_details(token, channel_id))

@APP.route('/channel/messages', methods=['GET'])
def recent_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return dumps(channel_messages(token, channel_id, start))

@APP.route('/channel/leave', methods=['POST'])
def leave_channel():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    return dumps(channel_leave(token, channel_id))

@APP.route('/channel/join', methods=['POST'])
def join_channel():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    return dumps(channel_join(token, channel_id))

@APP.route('/channel/addowner', methods=['POST'])
def addowner():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])
    return dumps(channel_addowner(token, channel_id, u_id))

@APP.route('/channel/removeowner', methods=['POST'])
def removeowner():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])
    return dumps(channel_removeowner(token, channel_id, u_id))

########################################
############ channels.py ###############
########################################
@APP.route('/channels/create', methods=['POST'])
def create_channel():
    data = request.get_json()
    token = data['token']
    name = data['name']
    is_public = bool(data['is_public'])
    return dumps(channels_create(token, name, is_public))

@APP.route('/channels/list', methods=['GET'])
def list_joined_channels():
    token = request.args.get('token')
    return dumps(channels_list(token))

@APP.route('/channels/listall', methods=['GET'])
def list_all_channels():
    token = request.args.get('token')
    return dumps(channels_listall(token))

########################################
############# message.py ###############
########################################
@APP.route('/message/send', methods=['POST'])
def send_message():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    msg = data['message']
    return dumps(message_send(token, channel_id, msg))

@APP.route('/message/remove', methods=['DELETE'])
def delete_message():
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    return dumps(message_remove(token, message_id))

@APP.route('/message/edit', methods=['PUT'])
def edit_message():
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    message = data['message']
    return dumps(message_edit(token, message_id, message))

########################################
############### user.py ################
########################################
@APP.route('/user/profile', methods=['GET'])
def get_profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return dumps(user_profile(token, u_id))

@APP.route('/user/profile/setname', methods=["PUT"])
def set_name():
    data = request.get_json()
    return dumps(user_profile_setname(data['token'], data['name_first'], data['name_last']))

@APP.route('/user/profile/setemail', methods=['PUT'])
def set_email():
    data = request.get_json()
    return dumps(user_profile_setemail(data['token'], data['email']))

@APP.route('/user/profile/sethandle', methods=['PUT'])
def set_handle():
    data = request.get_json()
    return dumps(user_profile_sethandle(data['token'], data['handle_str']))

########################################
############## other.py ################
########################################
@APP.route('/clear', methods=['DELETE'])
def clear_data():
    return dumps(clear())

@APP.route('/users/all' , methods=['GET'])
def get_all_users():
    return dumps(users_all(request.args.get('token')))

@APP.route('/admin/userpermission/change', methods=['POST'])
def change_permission():
    data = request.get_json()
    return dumps(admin_userpermission_change(data['token'],
            int(data['u_id']), int(data['permission_id'])))

@APP.route('/search', methods=['GET'])
def search_msg():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(search(token, query_str))

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
