from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
import jwt
from werkzeug.security import generate_password_hash, check_password_hash


allowed_users = {
    "carlos" : generate_password_hash("1234"),
    "andrea" : generate_password_hash("1234")    
}

allowed_token = {
    "token-carlos" :"sergio",
    "token-andrea" : "andrea"    
}


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')



@basic_auth.verify_password
def verify_password(username, password):
    if username in allowed_users and check_password_hash(allowed_users.get(username), password):
        return username

    return None

@token_auth.verify_token
def verify_token(token):
    try:
        decoded_jwt = jwt.decode(
            token,
            "mysecret", 
            algorithms=["HS256"])
    except Exception as e:
        return None
    
    if decoded_jwt["name"] in allowed_users:
        return decoded_jwt["name"]
    
    return None