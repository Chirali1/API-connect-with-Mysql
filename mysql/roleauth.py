from flask import request, jsonify
import jwt

# Define a list of routes that require authentication and roles
# Update this list with the routes and roles that need authentication in your application
routes_require_auth = [
    {'route': '/add_student', 'roles': ['mediator','admin']},
    {'route': '/students', 'roles': ['admin', 'user','mediator']},
    {'route':'/update_student', 'roles':'admin'},
    {'route':'/deletestudent','roles':'admin'},
    {'route':'/student','roles':['admin','user','mediator']}
]

def authmiddleware(app):
    @app.before_request
    def before_request():
        # Check if the requested route requires authentication and roles
        for route in routes_require_auth:
            if request.path == route['route']:
                # Perform authentication and role checks
                if not is_authenticated():
                    return jsonify({'message': 'Authentication required'}), 401

                if not has_required_role(route['roles']):
                    return jsonify({'message': 'Insufficient privileges'}), 403

def is_authenticated():
    # Implement your authentication logic here
    # This can involve checking the request headers, session cookies, tokens, or other authentication mechanisms
    # Return True if the user is authenticated, otherwise return False

    # Example: Check if the Authorization header contains a valid token
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        return is_valid_token(token) 

    return False

def is_valid_token(token):
    # Implement your token validation logic here
    # This can involve verifying the token signature, expiration, or checking against a database or cache
    # Return True if the token is valid, otherwise return False

    # Example: Perform token validation using a library like PyJWT
    try:
        jwt.decode(token, 'bcfc6ceab8bc4491b6a73da7f3b47c00' , algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def has_required_role(required_roles):
   
    user_role = get_user_role()
    if user_role in required_roles:
        return True

    return False

def get_user_role():
    # Implement your logic to retrieve the user's role
    # This can involve checking a database, session, or token payload
    # Return the user's role

    # Example: Retrieve the role from the token payload
    token = request.headers.get('Authorization').split(' ')[1]
    payload = jwt.decode(token, 'bcfc6ceab8bc4491b6a73da7f3b47c00', algorithms=['HS256'])
    return payload['role']
