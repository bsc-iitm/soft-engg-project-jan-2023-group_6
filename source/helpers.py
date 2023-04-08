from datetime import datetime, timedelta
from functools import wraps

from flask import request, make_response, jsonify
from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext

from models import User
from config import SECRET_KEY, ALGORITHM



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def generate_password_hash(password) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(auth_details: dict) -> dict:
    if not auth_details or not auth_details['username'] or not auth_details['password']:
        return make_response(jsonify('Could not verify. Missing username and/or password.', 401))
    user = User.query.filter_by(username=auth_details['username']).first()
    if not user:
        return make_response(jsonify('Could not verify. This username does not exist'), 401)
    
    token_data = {'username': user.username}
    access_token = create_access_token(token_data)
    user_details = {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'admin': True if user.admin == 1 else False
    }
    return {
        'user_details': user_details,
        'access_token': access_token,
        'token_type': 'bearer'
    }

def token_required(func):
    @wraps(func)
    def verify_token(*args, **kwargs):
        try:
            token = request.headers['Authorization'].split()[1]
            try:
                token_data = jwt.decode(token, SECRET_KEY, ALGORITHM)
                username = token_data['username']
            except ExpiredSignatureError:
                return make_response(jsonify("Session expired, please login again.", 440))
            except JWTError:
                return make_response(jsonify("Invalid credentials"), 401)
            current_user = User.query.filter_by(username=username).first()
            if current_user is None:
                return make_response(jsonify('Unauthorized request1'), 401)
            return func(current_user, *args, **kwargs)
        except:
            return make_response(jsonify('Unauthorized request2'), 401)
    return verify_token