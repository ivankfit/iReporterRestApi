from flask import Flask,json,jsonify,Blueprint,request
from app.views.incidents import incident
import datetime
import re

user = Blueprint('user', __name__)
users = []

@user.route('/api/v1/users', methods=['POST'])
def create_user():
    #### creates a new user
    if not request.content_type == 'application/json':
        return jsonify({"failed": "content-type must be application/json"}), 401
    request_data = request.get_json()
    try:
         if not is_valid(request_data['email']):
            return jsonify({"success": False, "msg": "Email is badly formatted"}), 401
    except KeyError as err:
         return jsonify({"success": False, "msg": "Email is missing"}), 400
    if not 'username' in request_data:
        return jsonify({'msg': 'User must have a username'}), 400
    if not 'firstname' in request_data:
        return jsonify({'msg': 'firstname must be provided'}), 400
    if not 'lastname' in request_data:
        return jsonify({'msg': 'lastname must be provided'}), 400
    
   
    newuser = {
        "user_id": len(users) + 1,
        "firstname":request_data['firstname'],
        "lastname":request_data['lastname'],
        "othernames":request_data['othernames'],
        "email":request_data['email'],
        "phone_number":request_data['phone_number'],
        "username":request_data['username'],
        "registered":datetime.datetime.utcnow(),
        "is_admin":False

    }
    if len(users) == 0:
        users.append(newuser)
        return jsonify({"success": True, "user_id": newuser.get('user_id') }), 201

    for user in users:
        if user['email'] == request_data['email']:
            return jsonify({"success": False, "msg": "Email is already taken"}), 409
        if user['username'] == request_data['username']:
            return jsonify({"success": False, "msg": "Username is already taken"}), 409
    users.append(newuser)
    return jsonify({"success": True, "user_id": newuser.get('user_id')}), 201

@user.route('/api/v1/users', methods=['GET'])
def getall_users():

    ####returns a list of all users
    if len(users) ==0:
        return jsonify({"msg": "No users yet", "count": len(users)}), 200

    return jsonify({"users": users, "count": len(users)}), 200



def is_valid(email): 
    match=re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email)
    return match



