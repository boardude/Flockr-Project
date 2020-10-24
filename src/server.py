import sys
from auth import auth_login, auth_logout, auth_register
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from other import clear

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
    input = request.get_json()
    return dumps(auth_login(input['email'], input['password']))

@APP.route('/auth/logout', methods=['POST'])
def logout():
    input = request.get_json()
    return dumps(auth_logout(input['token']))

@APP.route('/auth/register', methods=['POST'])
def register():
    input = request.get_json()
    return dumps(auth_register(input['email'], input['password'],
                    input['name_first'], input['name_last']))

########################################
############## other.py ################
########################################
@APP.route('/clear', methods=['DELETE'])
def clear_data():
    return dumps(clear())

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
