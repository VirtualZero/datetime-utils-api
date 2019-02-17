from functools import wraps
from datetimeapi import db, bcrypt
from datetimeapi.models.user import User
from flask import request, abort
import os
import jwt
import string
import random
import datetime
import pendulum


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {
                'Error': 'API key is required.'
            }, 401

        try:
            decoded_token = jwt.decode(token, os.environ["JWT_SECRET_KEY"])

            user = User.query.filter_by(
                email=decoded_token['email']
            ).first()

            if not user:
                return {
                    'Error': 'Not an active account.'
                }, 401

            if user.unique_id != decoded_token['unique_id'] or \
               user.api_key != token:
               return {
                   'Error': 'Invalid API Key.'
               }, 401

        except jwt.exceptions.DecodeError:
            return {
                'Error': 'Invalid API key.'
            }, 401

        except jwt.exceptions.ExpiredSignatureError:
            return {
                'Error': 'API key is expired.',
                'message': 'Use your refresh api key to update your API key.'
            }, 401

        except:
            abort(
                500,
                'Something went wrong.'
            )

        return f(*args, **kwargs)

    return decorated


def valid_email_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json()

        for i in data['recipients']:
            if '.' not in i or '@' not in i:
                abort(
                    401,
                    """At least one (1) invalid email address."""
                )

        return f(*args, **kwargs)

    return decorated


def create_account_creds_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        create_account_request = request.get_json()

        if not create_account_request:
            return {
                'Error:': 'Request must include email, password, and confirm_password.'
            }, 401

        if 'email' not in create_account_request or \
           'password' not in create_account_request or \
           'confirm_password' not in create_account_request:

           return {
               'Error:': 'Request must include email, password, and confirm_password.'
           }, 401

        if not create_account_request['email']:
            return {
                'Error:': 'Email address is required.'
            }, 401

        if not create_account_request['password']:
            return {
                'Error:': 'Password is required.'
            }, 401

        if not create_account_request['confirm_password']:
            return {
                'Error:': 'Password confirmation is required.'
            }, 401

        if create_account_request['password'] != create_account_request['confirm_password']:
            return {
                'Error:': 'Passwords must match.'
            }, 401

        if len(create_account_request['password']) < 8 or \
           len(create_account_request['password']) > 64:
            return {
                'Error:': 'Password must be between 8-64 characters.'
            }, 401

        if '@' not in create_account_request['email'] or \
           '.' not in create_account_request['email']:
           return {
               'Error:': 'Please enter a valid email address.'
           }, 401

        if User.query.filter_by(
            email=create_account_request['email']
        ).first():
            return {
                'Error:': 'That email address is already tied to an account.'
            }, 401

        return f(*args, **kwargs)

    return decorated


def create_new_user():
    data = request.get_json()

    unique = False
    unique_id = ""

    while unique == False:
        for i in range(8):
            unique_id = f"{unique_id}{random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)}"

        id_in_use = User.query.filter_by(
            unique_id=unique_id
        ).first()

        if not id_in_use:
            unique = True

    token = jwt.encode(
        {
            'email': data['email'],
            'unique_id': unique_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)
        },
        os.environ['JWT_SECRET_KEY']
    ).decode(
        'utf-8'
    )

    refresh_token = jwt.encode(
        {
            'email': data['email'],
            'unique_id': unique_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1500)
        },
        os.environ['JWT_REFRESH_KEY']
    ).decode(
        'utf-8'
    )

    new_user = User(
        unique_id=unique_id,
        email=data['email'],
        pw_hash=bcrypt.generate_password_hash(
            data['password']
        ).decode(
            'utf-8'
        ),
        api_key=token,
        refresh_api_key=refresh_token
    )

    new_user.commit_new_user()

    return {
        'status': 'Success',
        'message': 'Account Created',
        'important': 'Your API key will expire in 365 days.',
        'get_new_api_key': 'POST https://geons.virtualzero.tech/get-new-api-key',
        'get_new_api_key_required': 'Email, Password, Headers=key: X-API-KEY, value: YOUR_REFRESH_API_KEY',
        'api_key': new_user.api_key,
        'refresh_api_key': new_user.refresh_api_key
    }


def validate_convert_timezones_data():
    data = request.get_json()

    try:
        timestamp = data['timestamp'].strip()

    except KeyError:
        return {
            'status': 'Failure',
            'error': "'timestamp' is a required field."
        }

    try:
        valid_datetime = pendulum.parse(data['timestamp'])

    except pendulum.parsing.exceptions.ParserError:
        return {
            'status': 'Failure',
            'error': 'Could not parse timestamp.'
        }

    except:
        return {
            'status': 'Failure',
            'error': 'Invalid or malformed timestamp.'
        }
        
    try:
        from_tz = data['from'].strip()

    except KeyError:
        return {
            'status': 'Failure',
            "error": "'from' is a required field."
        }

    try:
        valid_from = valid_datetime.in_timezone(from_tz)

    except:
        return {
            'status': 'Failure',
            "error": "Invalid timezone in 'from' field."
        }

    try:
        to_tz = data['to']

    except KeyError:
        return {
            'status': 'Failure',
            "error": "'to' is a required field."
        }

    valid_to_list = []

    for to in to_tz:
        try:
            valid_to = valid_datetime.in_timezone(to)
            valid_to_list.append(to)

        except:
            pass

    if not valid_to_list:
        return {
            'status': 'Failure',
            'error': 'No valid timezones passed with the request.'
        }

    return {
        'timestamp': timestamp,
        'from': from_tz,
        'to': valid_to_list
    }


def refresh_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {
                'Error': 'Refresh API key is required.'
            }, 401

        try:
            decoded_token = jwt.decode(token, os.environ["JWT_REFRESH_KEY"])

            user = User.query.filter_by(
                email=decoded_token['email']
            ).first()

            if not user:
                return {
                    'Error': 'Not an active account.'
                }, 401

            if user.unique_id != decoded_token['unique_id'] or \
               user.refresh_api_key != token:
               return {
                   'Error': 'Access denied.'
               }, 401

        except jwt.exceptions.DecodeError:
            return {
                'Error': 'Invalid refresh API key.'
            }, 401

        except:
            abort(
                500,
                'Something went wrong.'
            )

        return f(*args, **kwargs)

    return decorated


def validate_math_timezones(timezones, valid_datetime):
    if not timezones:
        return []

    valid_timezones = []

    for timezone in timezones:
        try:
            valid_timezone = valid_datetime.in_timezone(timezone)
            valid_timezones.append(timezone)

        except:
            pass

    return valid_timezones


def make_new_api_key():
    token = request.headers['X-API-KEY']
    decoded_token = jwt.decode(token, os.environ["JWT_REFRESH_KEY"])

    user = User.query.filter_by(
        email=decoded_token['email']
    ).first()

    new_token = token = jwt.encode(
        {
            'email': user.email,
            'unique_id': user.unique_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)
        },
        os.environ['JWT_SECRET_KEY']
    ).decode(
        'utf-8'
    )

    user.api_key = new_token
    db.session.flush()
    db.session.commit()

    return {
        'status': 'success',
        'new_api_key': user.api_key
    }


def creds_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key_request = request.get_json()

        if not key_request:
            return {
                'Error:': 'Request must include your email and password.'
            }, 401

        if 'email' not in key_request or \
           'password' not in key_request:

           return {
               'Error:': 'Request must include your email and password.'
           }, 401

        if not key_request['email']:
            return {
                'Error:': 'Email address is required.'
            }, 401

        if not key_request['password']:
            return {
                'Error:': 'Password is required.'
            }, 401

        if len(key_request['password']) < 8 or \
           len(key_request['password']) > 64:
            return {
                'Error:': 'Password must be between 8-64 characters.'
            }, 401

        if '@' not in key_request['email'] or \
           '.' not in key_request['email']:
           return {
               'Error:': 'Please enter a valid email address.'
           }, 401

        user = User.query.filter_by(
            email=key_request['email']
        ).first()

        if not user:
            return {
                'Error:': 'Incorrect email address.'
            }, 401

        if not bcrypt.check_password_hash(
            user.pw_hash,
            key_request['password']
        ):
            return {
                'Error': 'Incorrect password.'
            }

        return f(*args, **kwargs)

    return decorated


def get_api_keys():
    key_request = request.get_json()
    
    user = User.query.filter_by(
        email=key_request['email']
    ).first()

    return {
        'status': 'Success',
        'api_key': user.api_key,
        'refresh_api_key': user.refresh_api_key
    }


def make_new_refresh_api_key():
    key_request = request.get_json()

    user = User.query.filter_by(
        email=key_request['email']
    ).first()

    new_refresh_token = jwt.encode(
        {
            'email': user.email,
            'unique_id': user.unique_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1500)
        },
        os.environ['JWT_REFRESH_KEY']
    ).decode(
        'utf-8'
    )

    user.refresh_api_key = new_refresh_token
    db.session.commit()

    return {
        'status': 'Success',
        'new_refresh_api_key': user.refresh_api_key
    }


def update_password():
    update_password_request = request.get_json()

    if len(update_password_request['new_password'].strip()) < 8 or \
       len(update_password_request['new_password'].strip()) > 64:
        return {
            'Error:': 'New password must be between 8-64 characters.'
        }, 401

    user = User.query.filter_by(
        email=update_password_request['email']
    ).first()

    user.pw_hash = bcrypt.generate_password_hash(
        update_password_request['new_password']
    ).decode(
        'utf-8'
    )

    db.session.commit()

    return {
        'status': 'Success',
        'message': 'Your password has been updated.'
    }
