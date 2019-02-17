from flask import request, abort
from datetimeapi import app
from datetimeapi import db
from flask_restplus import Api, Resource, fields
from datetimeapi.models.user import User
import jwt
import pendulum
import datetime
from datetimeapi.api.helpers.current_timestamp_helpers import (
    prepare_current_timestamp_response
)
from datetimeapi.api.helpers.convert_timezones_helpers import (
    convert_timezones
)
from datetimeapi.api.helpers.addition_helpers import (
    add_time
)
from datetimeapi.api.helpers.subtraction_helpers import (
    subtract_time
)
from datetimeapi.api.helpers.difference_helpers import (
    get_difference
)
from datetimeapi.api.helpers.description_text import (
    api_description_text,
    ns_datetime_description_text,
    ns_user_description_text,
    get_current_timestamp_description_text,
    create_account_description_text,
    convert_timezones_description_text,
    addition_description_text,
    subtraction_description_text,
    difference_description_text,
    get_new_api_key_description_text,
    forgot_api_keys_description_text,
    get_new_refresh_api_key_description_text,
    update_password_description_text
)
from datetimeapi.api.helpers.api_helpers import (
    token_required,
    valid_email_required,
    create_account_creds_required,
    create_new_user,
    validate_convert_timezones_data,
    refresh_token_required,
    make_new_api_key,
    creds_required,
    get_api_keys,
    make_new_refresh_api_key,
    update_password
)


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    app,
    authorizations=authorizations,
    title='VIRTUALZERO DATETIME UTILITIES API',
    version='1.0',
    description=api_description_text(),
    validate=True
)


# Namespaces
ns_datetime = api.namespace(
    'datetime',
    description=ns_datetime_description_text()
)

ns_user = api.namespace(
    'user',
    description=ns_user_description_text()
)


# API Models
new_api_user = ns_user.model(
    'NewUser',
    {
        'email': fields.String('email', required=True),
        'password': fields.String('password', required=True),
        'confirm_password': fields.String('confirm_password', required=True)
    }
)

api_user = ns_user.model(
    'User',
    {
        'email': fields.String('email', required=True),
        'password': fields.String('password', required=True)
    }
)

new_password = ns_user.model(
    'UpdatePassword',
    {
        'email': fields.String('email', required=True),
        'password': fields.String('password', required=True),
        'new_password': fields.String('password', required=True)
    }
)

timezone_convert = ns_datetime.model(
    'TimezoneConvert',
    {   
        'timestamp': fields.String('timestamp', required=True),
        'from': fields.String('current timezone', required=True),
        'to': fields.List(fields.String, required=True)
    }
)

addition = ns_datetime.model(
    'Addition',
    {
        'timestamp': fields.String('timestamp', required=True),
        'years': fields.Integer('years', required=True),
        'months': fields.Integer('months', required=True),
        'days': fields.Integer('days', required=True),
        'weeks': fields.Integer('weeks', required=True),
        'hours': fields.Integer('hours', required=True),
        'minutes': fields.Integer('minutes', required=True),
        'seconds': fields.Integer('seconds', required=True),
        'timezones': fields.List(fields.String)
    }
)

subtraction = ns_datetime.model(
    'Subtraction',
    {
        'timestamp': fields.String('timestamp', required=True),
        'years': fields.Integer('years', required=True),
        'months': fields.Integer('months', required=True),
        'days': fields.Integer('days', required=True),
        'weeks': fields.Integer('weeks', required=True),
        'hours': fields.Integer('hours', required=True),
        'minutes': fields.Integer('minutes', required=True),
        'seconds': fields.Integer('seconds', required=True),
        'timezones': fields.List(fields.String)
    }
)

difference = ns_datetime.model(
    'Difference',
    {
        'timestamp1': fields.String('timestamp1', required=True),
        'timestamp2': fields.String('timestamp2')
    }
)


# Endpoints


@ns_datetime.route('/get-current-timestamp')
class GetCurrentTimestamp(Resource):
    @ns_datetime.header(
        'X-API-KEY',
        'Must include the API key in the header.'
    )
    @ns_datetime.doc(
        description=get_current_timestamp_description_text()
    )
    @ns_datetime.doc(security='apikey')
    @ns_datetime.doc(
        responses={
            200: 'Success',
            401: 'Not Authorized',
            500: 'Something went wrong.'
        })
    @ns_datetime.doc(
        params={
            'tz': 'Desired timezone (e.g. America/New_York), else blank.',
            'elements': 'False to exclude elements, else blank.',
            'only_elements': 'True to exclude timestamps, else blank.'
        }
    )
    @token_required
    def get(self):
        return {
            'status': 'success',
            'current_timestamps': prepare_current_timestamp_response()
        }, 200


@ns_datetime.route('/convert-timezones')
class ConvertTimezones(Resource):
    @ns_datetime.header(
        'X-API-KEY',
        'Must include the API key in the header.'
    )
    @ns_datetime.doc(
        description=convert_timezones_description_text()
    )
    @ns_datetime.doc(security='apikey')
    @ns_datetime.doc(
        responses={
            200: 'Success',
            401: 'Not Authorized',
            500: 'Something went wrong.'
        })
    @ns_datetime.doc(
        params={
            'elements': 'False to exclude elements, else blank.',
            'only_elements': 'True to exclude timestamps, else blank.'
        }
    )
    @ns_datetime.expect(timezone_convert)
    @token_required
    def post(self):
        convert_tz_data = validate_convert_timezones_data()

        try:
            error = convert_tz_data['error']
            return convert_tz_data

        except:
            pass

        return convert_timezones(convert_tz_data), 200

@ns_datetime.route('/addition')
class Addition(Resource):
    @ns_datetime.header(
        'X-API-KEY',
        'Must include the API key in the header.'
    )
    @ns_datetime.doc(
        description=addition_description_text()
    )
    @ns_datetime.doc(security='apikey')
    @ns_datetime.doc(
        responses={
            200: 'Success',
            401: 'Not Authorized',
            500: 'Something went wrong.'
        })
    @ns_datetime.doc(
        params={
            'elements': 'False to exclude elements, else blank.',
            'only_elements': 'True to exclude timestamps, else blank.',
            'timestamp_now': 'True to use current timestamp, else blank'
        }
    )
    @ns_datetime.expect(addition)
    @token_required
    def post(self):
        return add_time(), 200


@ns_datetime.route('/subtraction')
class Subtraction(Resource):
    @ns_datetime.header(
        'X-API-KEY',
        'Must include the API key in the header.'
    )
    @ns_datetime.doc(
        description=subtraction_description_text()
    )
    @ns_datetime.doc(security='apikey')
    @ns_datetime.doc(
        responses={
            200: 'Success',
            401: 'Not Authorized',
            500: 'Something went wrong.'
        })
    @ns_datetime.doc(
        params={
            'elements': 'False to exclude elements, else blank.',
            'only_elements': 'True to exclude timestamps, else blank.',
            'timestamp_now': 'True to use current timestamp, else blank'
        }
    )
    @ns_datetime.expect(subtraction)
    @token_required
    def post(self):
        return subtract_time(), 200


@ns_datetime.route('/difference')
class Difference(Resource):
    @ns_datetime.header(
        'X-API-KEY',
        'Must include the API key in the header.'
    )
    @ns_datetime.doc(
        description=difference_description_text()
    )
    @ns_datetime.doc(security='apikey')
    @ns_datetime.doc(
        responses={
            200: 'Success',
            401: 'Not Authorized',
            500: 'Something went wrong.'
        }
    )
    @ns_datetime.expect(difference)
    @token_required
    def post(self):
        return get_difference(), 200


@ns_user.route('/create-account')
class GetCurrentTimestamp(Resource):
    @ns_user.expect(new_api_user)
    @ns_user.doc(
        description=create_account_description_text()
    )
    @ns_user.doc(
        responses={
            200: 'Success',
            401: 'Not Authorized',
            500: 'Something went wrong.'
        })
    @create_account_creds_required
    def post(self):
        return create_new_user(), 200


@ns_user.route('/get-new-api-key')
class GetNewAPIKey(Resource):
    @ns_user.doc(
        description=get_new_api_key_description_text()
    )
    @ns_user.doc(security='apikey')
    @ns_user.header(
        'X-API-KEY', 
        'Must include the refresh API key in header.'
    )
    @ns_user.doc(
        responses={
            200: 'Success', 
            401: 'Not Authorized', 
            500: 'Something went wrong.'
        }
    )
    @refresh_token_required
    def get(self):
        return make_new_api_key(), 200


@ns_user.route('/forgot-api-keys')
class ForgotAPIKeys(Resource):
    @ns_user.doc(
        description=forgot_api_keys_description_text()
    )
    @ns_user.expect(api_user)
    @ns_user.doc(
        responses={
            200: 'Success', 
            401: 'Not Authorized', 
            500: 'Something went wrong.'
        }
    )
    @creds_required
    def post(self):
        return get_api_keys(), 200


@ns_user.route('/get-new-refresh-api-key')
class GetNewRefreshAPIKey(Resource):
    @ns_user.doc(
        description=get_new_refresh_api_key_description_text()
    )
    @ns_user.expect(api_user)
    @ns_user.doc(
        responses={
            200: 'Success', 
            401: 'Not Authorized', 
            500: 'Something went wrong.'
        }
    )
    @creds_required
    def post(self):
        return make_new_refresh_api_key(), 200


@ns_user.route('/update-password')
class UpdatePassword(Resource):
    @ns_user.doc(
        description=update_password_description_text()
    )
    @ns_user.expect(new_password)
    @ns_user.doc(
        responses={
            200: 'Success',
            401: 'Not Authorized',
            500: 'Something went wrong.'
        }
    )
    @creds_required
    def post(self):
        return update_password(), 200
