from flask import request
import pendulum
import datetime

def convert_timezones(data):
    elements = request.args.get('elements')
    only_elements = request.args.get('only_elements')
    response_payload = {}

    tos = data['to']
    
    for to in tos:
        timestamp = pendulum.parse(data['timestamp'], tz=data['from'])
        converted_timestamp = timestamp.in_timezone(to)

        if not only_elements or only_elements.lower() != 'true':
            response_payload[to] = {
                'timezone_aware': str(converted_timestamp),
                'iso_8601_format': converted_timestamp.to_iso8601_string(),
                'atom': converted_timestamp.to_atom_string(),
                'cookie': converted_timestamp.to_cookie_string(),
                'rss': converted_timestamp.to_rss_string(),
                'w3c': converted_timestamp.to_w3c_string(),
                'datetime': {
                    'datetime_string': converted_timestamp.to_datetime_string(),
                    'date_string': converted_timestamp.to_date_string(),
                    'time_string': converted_timestamp.to_time_string()
                },

                'rfc': {
                    'rfc822': converted_timestamp.to_rfc822_string(),
                    'rfc850': converted_timestamp.to_rfc850_string(),
                    'rfc1036': converted_timestamp.to_rfc1036_string(),
                    'rfc1123': converted_timestamp.to_rfc1123_string(),
                    'rfc2822': converted_timestamp.to_rfc2822_string(),
                    'rfc3339': converted_timestamp.to_rfc3339_string()
                },

                'epoch': {
                    'float': converted_timestamp.float_timestamp,
                    'integer': converted_timestamp.int_timestamp
                },

                'pretty': {
                    '12_hour': datetime.datetime.strftime(
                        converted_timestamp,
                        '%D %-I:%M %p'
                    ),
                    '24_hour': datetime.datetime.strftime(
                        converted_timestamp,
                        '%D %H:%M'
                    )
                },

                'descriptive': {
                    '12_hour': datetime.datetime.strftime(
                        converted_timestamp,
                        '%A, %B %-d, %Y %-I:%M %p'
                    ),
                    '24_hour': datetime.datetime.strftime(
                        converted_timestamp,
                        '%A, %B %-d, %Y %H:%M'
                    )
                }
            }

        else:
            response_payload[to] = {}

        if not elements or elements.lower() != 'false':
                response_payload[to]['elements'] = {
                    'date': {
                        'day': {
                            'weekday': {
                                'full': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%A'
                                ),
                                'abbreviated': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%a'
                                ),
                                'number': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%w'
                                )
                            },

                            'day_of_month_zero_padded': datetime.datetime.strftime(
                                converted_timestamp,
                                '%d'
                            ),
                            'day_of_month_non_zero_padded': datetime.datetime.strftime(
                                converted_timestamp,
                                '%-d'
                            ),

                            'day_of_year': converted_timestamp.day_of_year
                        },

                        'week': {
                            'week_of_year': converted_timestamp.isocalendar()[1],
                            'week_of_month': converted_timestamp.week_of_month
                        },

                        'month': {
                            'full_name': datetime.datetime.strftime(
                                converted_timestamp,
                                '%B'
                            ),
                            'abbreviated_name': datetime.datetime.strftime(
                                converted_timestamp,
                                '%b'
                            ),
                            
                        },
                        'year': {
                            'without_century': datetime.datetime.strftime(
                                converted_timestamp,
                                '%y'
                            ),
                            'with_century': datetime.datetime.strftime(
                                converted_timestamp,
                                '%Y'
                            )
                        },

                        'quarter': converted_timestamp.quarter
                    },

                    'time': {
                        '24_hour': {
                            'hour': {
                                'zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%H'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%-H'
                                )
                            },
                            'minute': {
                                'zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%M'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%-M'
                                )
                            },
                            'second': {
                                'zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%S'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%S'
                                )
                            },
                            'milisecond': datetime.datetime.strftime(
                                converted_timestamp,
                                '%f'
                            )

                        },

                        '12_hour': {
                            'hour': {
                                'zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%I'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%-I'
                                )
                            },

                            'minute': {
                                'zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%M'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%-M'
                                )
                            },

                            'second': {
                                'zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%S'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    converted_timestamp,
                                    '%S'
                                )
                            },

                            'milisecond': datetime.datetime.strftime(
                                converted_timestamp,
                                '%f'
                            ),

                            'am_pm': datetime.datetime.strftime(
                                converted_timestamp,
                                '%p'
                            ),
                        },
                        'timezone': converted_timestamp.timezone_name
                    },

                    'timezone_offset': datetime.datetime.strftime(
                        converted_timestamp,
                        '%z'
                    )
                }
    
    if len(data['to']) < len(request.get_json()['to']):
        response_payload['errors'] = 'At least one invalid timezone passed in the request.'

    return {
        'status': 'Success',
        'converted_data': response_payload
    }
