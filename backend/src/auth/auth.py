"""auth.py

This is an authentication module using Auth0 for
the Flask app: Coffee Shop Full Stack'.
.
- Author: Mason Kim (icegom@gmail.com)
- Start code is provided by Udacity

Example:
    from .auth.auth import requires_auth

    # Use 'requires_auth" as a decorator function
    @app.route('/drinks-detail', methods=['GET'])
    @requires_auth('get:drinks-detail')
    def retrieve_drinks_detail(payload):
        pass
"""

import json
from flask import abort, request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'masonkim32.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffeeShop'


class AuthError(Exception):
    """A standardized way to communicate auth failure modes

    Arguments::
        error (dict): code, and description of the error
        status_code (int): HTTP response status codes
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the access token from the Authorization Header.

    It should attempt to get the header from the request and split
    bearer and the token.

    Returns:
        str: the token part of the header

    Raises:
        AuthError: [401, authorization_header_missing] Authorization
                head is expected.
        AuthError: [401, invalid_header] Authorization head must
                start with "Bearer".
        AuthError: [invalid_header] Token not found
        AuthError: [invalid_header] Authorization header must be
                bearer token.
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization head is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization head must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
        })

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        })

    token = parts[1]
    print('Token type: ', type(token))
    return token


def check_permissions(permission, payload):
    """Check whether the permissions of logged-in users are valid.

    Arguments:
        permission (str): permission (i.e. 'post:drink')
        payload (dict): decoded jwt payload

    Returns:
        bool: True if permissions are included in the payload and
            the requested permission is in the array of the payload
            permissions.

    Raises:
        AuthError: [400, invalid_claims] Permissions not included
                in JWT.
        AuthError: [403, Unauthorized] Permission not found.
    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permission not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


def verify_decode_jwt(token):
    """Verify jwt token and return decoded payload

    Arguments:
        token (str): a json web token

    Returns:
        dict: The decoded payload.

    Raises:
        AuthError: [401, invalid_header] Authorization malformed.
        AuthError: [401, token_expired] Token expired.
        AuthError: [401, invalid_claims] Incorrect claims. Please,
                check the audience and issuer.
        AuthError: [400, invalid_header] Unable to parse
                authentication token.
        AuthError: [400, invalid_header] Unable to find the
                appropriate key.
    """
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(permission=''):
    """Implementation of @requires_auth(permission) decorator method

    Get the jwt token and decoded it. Then check if the permission
    of the token is valid.

    Keyword Arguments:
        permission (str): permission (i.e. 'post:drink')

    Returns:
        func: the decorator which passes the decoded payload to
            the decorated method
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)

            except AuthError as err:
                abort(401, err.error)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
