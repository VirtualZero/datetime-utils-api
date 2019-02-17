def get_current_timestamp_description_text():
    return """<p style='font-size: 16px;'>Make a GET request to 
    this route to retrieve the current timestamp. Default timestamp 
    is UTC with additional timezones specified by query string 
    parameters. Specify timezones by using tz=DESIRED_TIMEZONE as 
    a query string parameter. To retrieve data for multiple timezones, 
    simply use multiple tz= parameters in the query string. If no 
    timezones are specified in the query string, the API will return 
    data in UTC only. Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/get-current-timestamp?tz=America/New_York&tz=America/Denver</a>. 
    The default action of the API is to return all of the individual 
    elements that the timestamp is comprised of, in addition to the 
    actual timestamps. To retrieve ONLY the actual timestamps 
    (without the elements), simply use elements=False as a query 
    string parameter. Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/get-current-timestamp?tz=America/New_York&elements=False</a>. 
    To exclude timestamps and retrieve ONLY the elements that the 
    timestamp is comprised of, simply use only_elements=True as a 
    query string parameter. Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/get-current-timestamp?tz=America/New_York&only_elements=True</a>. 
    For obvious reasons, if both only_elements=True and elements=False 
    are used as query string parameters, the API will return a 
    successful response, but the response will contain no data.</p>"""


def api_description_text():
    return """A RESTful API that provides datetime formatting, timezone \
    conversion, and datetime calculation services to independent \
    applications. This API is open source and the code can be viewed or \
    cloned <a href='https://git.virtualzero.tech/VirtualZero/datetime-utils-api' target='_blank'>\
    here</a>."""


def ns_datetime_description_text():
    return """The datetime namespace contains the routes used for \
    retrieving datetime information from the API. <a href='#'>Click \
    here</a> to view the routes."""


def ns_user_description_text():
    return """The user namespace contains the routes for user \
    operations, such as creating an account, refreshing an API key, \
    etc. <a href='#'>Click here</a> to view the routes."""


def create_account_description_text():
    return """<p style='font-size: 16px;'>Make a POST request to 
    this route to create an account. The request must include a 
    valid email address and matching password and confirm_password 
    fields as the request payload. Upon successful account creation, 
    the API will return an API key and refresh API key as the 
    response payload. You must use the API key when requesting 
    datetime data from the API. The API key will expire in 365 days. 
    You must use your refresh API key to obtain a new API key.</p>"""


def convert_timezones_description_text():
    return """<p style='font-size: 16px;'>Make a POST request to 
    this route to convert a timestamp from one timezone to another. 
    The request must include a valid timestamp, a 'from' timezone, 
    a 'to' timezone (list), and the API key in the header. The API 
    supports timestamps in RFC 3339, most ISO 8601 formats, and a 
    few other common formats. Some examples of valid timestamps are 
    2019-02-03T18:16:38-05:00 and 2019-02-03 18:16:38. The default 
    action of the API is to return all of the individual elements 
    that the timestamp is comprised of, in addition to the actual 
    timestamps. To retrieve ONLY the actual timestamps 
    (without the elements), simply use elements=False as a query 
    string parameter. Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/convert-timezones?elements=False</a>. 
    To exclude timestamps and retrieve ONLY the elements that the 
    timestamp is comprised of, simply use only_elements=True as a query 
    string parameter. Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/convert-timezones?only_elements=True</a>. 
    For obvious reasons, if both only_elements=True and elements=False 
    are used as query string parameters, the API will return a 
    successful response, but the response will contain no data.</p>"""


def addition_description_text():
    return """<p style='font-size: 16px;'>Make a POST request to 
    this route to add units of time to a timestamp. The request must 
    include a vaild UTC timestamp, the API key in the header, and 
    all units of time to add to the timestamp. For units of time that 
    you do not wish to use, simply set their value to 0 (zero) in 
    the request payload. The units of time are 'years', 'months', 
    'days', 'weeks', 'hours', 'minutes', and 'seconds'. By default, 
    the API will return the updated timestamp in UTC only. To specify
    additional timezones, add the optional 'timezones' field to the 
    request payload. This field accepts a list of timezones. The API 
    supports timestamps in RFC 3339, most ISO 8601 formats, and a 
    few other common formats. Some examples of valid timestamps are 
    2019-02-03T18:16:38-05:00 and 2019-02-03 18:16:38. To add units 
    of time to a current timestamp instead of sending a timestamp 
    in the request, simply use timestamp_now=true as a query string 
    parameter and set the value of timestamp in the request payload 
    to 0 (zero). Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/addition?timestamp_now=True</a> 
    The default action of the API is to return all of the individual 
    elements that the timestamp is comprised of, in addition to the 
    actual timestamps. To retrieve ONLY the actual timestamps 
    (without the elements), simply use elements=False as a query 
    string parameter. Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/addition?elements=False</a>. 
    To exclude timestamps and retrieve ONLY the elements that the 
    timestamp is comprised of, simply use only_elements=True as a 
    query string parameter. Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/addition?only_elements=True</a>. 
    For obvious reasons, if both only_elements=True and elements=False 
    are used as query string parameters, the API will return a 
    successful response, but the response will contain no data.</p>"""


def subtraction_description_text():
    return """<p style='font-size: 16px;'>Make a POST request to 
    this route to subtract units of time from a timestamp. The request must 
    include a vaild UTC timestamp, the API key in the header, and 
    all units of time to subtract from the timestamp. For units of time that 
    you do not wish to use, simply set their value to 0 (zero) in 
    the request payload. The units of time are 'years', 'months', 
    'days', 'weeks', 'hours', 'minutes', and 'seconds'. By default, 
    the API will return the updated timestamp in UTC only. To specify
    additional timezones, add the optional 'timezones' field to the 
    request payload. This field accepts a list of timezones. The API 
    supports timestamps in RFC 3339, most ISO 8601 formats, and a 
    few other common formats. Some examples of valid timestamps are 
    2019-02-03T18:16:38-05:00 and 2019-02-03 18:16:38. To add units 
    of time to a current timestamp instead of sending a timestamp 
    in the request, simply use timestamp_now=true as a query string 
    parameter and set the value of timestamp in the request payload 
    to 0 (zero). Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/addition?timestamp_now=True</a> 
    The default action of the API is to return all of the individual 
    elements that the timestamp is comprised of, in addition to the 
    actual timestamps. To retrieve ONLY the actual timestamps 
    (without the elements), simply use elements=False as a query 
    string parameter. Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/addition?elements=False</a>. 
    To exclude timestamps and retrieve ONLY the elements that the 
    timestamp is comprised of, simply use only_elements=True as a 
    query string parameter. Example: 
    <a href="#">https://datetimeapi.virtualzero.tech/datetime/addition?only_elements=True</a>. 
    For obvious reasons, if both only_elements=True and elements=False 
    are used as query string parameters, the API will return a 
    successful response, but the response will contain no data.</p>"""


def difference_description_text():
    return """<p style='font-size: 16px;'>Make a POST request to 
    this route to find the difference between 2 timestamps. The request must 
    include at least one valid timestamp and the API key in the header. If 
    only one timestamp is included in the request, the difference calculation 
    will be performed using the included timestamp and the current timestamp. 
    If the optional 'timestamp2' field is included in the request and the 
    timestamp is valid, the calculation will be performed using the two included 
    timestamps. To ensure accuracy in the calculation, it is recommended to 
    include UTC timestamps in the request, however, if the timestamps included in 
    the request are timezone aware, the calculation will also be accurate. If 
    two timestamps are included in the request and they are not UTC, make sure 
    that they are from the same timezone at least. The API 
    supports timestamps in RFC 3339, most ISO 8601 formats, and a 
    few other common formats. Some examples of valid timestamps are 
    2019-02-03T18:16:38-05:00 and 2019-02-03 18:16:38.</p>"""


def get_new_api_key_description_text():
    return """<p style='font-size: 16px;'>Obtain a new API key by making a GET 
    request to this route. The request must include the refresh API key in the 
    header. The new API key will be returned in the response payload and the 
    old API key will be invalidated immediately.</p>"""


def forgot_api_keys_description_text():
    return """<p style='font-size: 16px;'>If you lose your API keys, make a 
    POST request to this route. The request must contain the email address 
    and password that the account was created with. The API will return the 
    API key and refresh API as the response payload.</p>"""


def get_new_refresh_api_key_description_text():
    return """<p style='font-size: 16px;'>Obtain a new refresh API key by 
    making a POST request to this route. The request must contain the email 
    address that the account was created with and the current account password. 
    The new refresh API key will be returned as the response payload and the 
    old refresh API key will be invalidated immediately.</p>"""


def update_password_description_text():
    return """<p style='font-size: 16px;'>Make a POST request to this route 
    to update a password. The request must contain the email address that the 
    account was created with, the current account password, and a 'new_password' 
    field containing the desired new password. The new password must be between 
    8-64 characters. Upon successful completion of the request, the API will 
    return a success message and the old password will be invalidated 
    immediately.</p>"""
