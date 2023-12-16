from flask import request, jsonify
import jwt

SECRET_KEY = 'bcfc6ceab8bc4491b6a73da7f3b47c00'

excluded_routes = ['/login']

def jwtmiddleware(app):
    @app.before_request

    def before_request():
        # Exclude certain routes from token verification, if needed
        excluded_routes = ['/login','/students','/deletestudent','/update_student','/student','/add_student']

        if request.path in excluded_routes:
            # Perform authentication checks
            if not is_authenticated():
                return jsonify({'message': 'Authentication required'}), 401

def is_authenticated():
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            return is_valid_token(token)

        return False

def is_valid_token(token):
    
    try:
        jwt.decode(token, 'bcfc6ceab8bc4491b6a73da7f3b47c00', algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False