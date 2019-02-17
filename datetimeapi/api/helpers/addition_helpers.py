from flask import request
import pendulum
import datetime
from datetimeapi.api.helpers.api_helpers import (
    validate_math_timezones
)


def add_time():
    elements = request.args.get('elements')
    only_elements = request.args.get('only_elements')
    data = request.get_json()
    valid_datetime = ""

    if request.args.get('timestamp_now'):
        if request.args.get('timestamp_now').lower() == 'true':
                valid_datetime = pendulum.now("UTC")

    if valid_datetime == "":
        try:
            valid_datetime = pendulum.parse(data['timestamp']).in_timezone('UTC')

        except pendulum.parsing.exceptions.ParserError:
            return {
                'status': 'Failure',
                'error': 'Could not parse timestamp.'
            }

    converted_timestamp = valid_datetime.add(
        days=data['days'],
        hours=data['hours'],
        minutes=data['minutes'],
        seconds=data['seconds'],
        months=data['months'],
        weeks=data['weeks'],
        years=data['years']
    )

    response_payload = {
        'UTC': {

        }
    }

    if not only_elements or only_elements.lower() != 'true':
        response_payload['UTC'] = {
            'timezone_aware': str(converted_timestamp),
            'iso_8601_format': converted_timestamp.to_iso8601_string(),
            'atom': converted_timestamp.to_atom_string(),
            'cookie': converted_timestamp.to_cookie_string(),
            'rss': converted_timestamp.to_rss_string(),
            'w3c': converted_timestamp.to_w3c_string(),
            'human_readable': valid_datetime.add(
                days=data['days'],
                hours=data['hours'],
                minutes=data['minutes'],
                seconds=data['seconds'],
                months=data['months'],
                weeks=data['weeks'],
                years=data['years']
            ).diff_for_humans(),

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

    if not elements or elements.lower() != 'false':
            response_payload['UTC']['elements'] = {
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

    try:
        timezones = validate_math_timezones(data['timezones'], valid_datetime)

    except:
        timezones = []

    if timezones:
        for timezone in timezones:
            addition_in_tz = converted_timestamp.in_timezone(timezone)

            if not only_elements or only_elements.lower() != 'true':
                response_payload[timezone] = {
                    'timezone_aware': str(addition_in_tz),
                    'iso_8601_format': addition_in_tz.to_iso8601_string(),
                    'atom': addition_in_tz.to_atom_string(),
                    'cookie': addition_in_tz.to_cookie_string(),
                    'rss': addition_in_tz.to_rss_string(),
                    'w3c': addition_in_tz.to_w3c_string(),
                    'human_readable': valid_datetime.add(
                        days=data['days'],
                        hours=data['hours'],
                        minutes=data['minutes'],
                        seconds=data['seconds'],
                        months=data['months'],
                        weeks=data['weeks'],
                        years=data['years']
                    ).in_timezone(timezone).diff_for_humans(),

                    'datetime': {
                        'datetime_string': addition_in_tz.to_datetime_string(),
                        'date_string': addition_in_tz.to_date_string(),
                        'time_string': addition_in_tz.to_time_string()
                    },

                    'rfc': {
                        'rfc822': addition_in_tz.to_rfc822_string(),
                        'rfc850': addition_in_tz.to_rfc850_string(),
                        'rfc1036': addition_in_tz.to_rfc1036_string(),
                        'rfc1123': addition_in_tz.to_rfc1123_string(),
                        'rfc2822': addition_in_tz.to_rfc2822_string(),
                        'rfc3339': addition_in_tz.to_rfc3339_string()
                    },

                    'epoch': {
                        'float': addition_in_tz.float_timestamp,
                        'integer': addition_in_tz.int_timestamp
                    },

                    'pretty': {
                        '12_hour': datetime.datetime.strftime(
                            addition_in_tz,
                            '%D %-I:%M %p'
                        ),
                        '24_hour': datetime.datetime.strftime(
                            addition_in_tz,
                            '%D %H:%M'
                        )
                    },

                    'descriptive': {
                        '12_hour': datetime.datetime.strftime(
                            addition_in_tz,
                            '%A, %B %-d, %Y %-I:%M %p'
                        ),
                        '24_hour': datetime.datetime.strftime(
                            addition_in_tz,
                            '%A, %B %-d, %Y %H:%M'
                        )
                    }
                }

            else:
                response_payload[timezone] = {}

            if not elements or elements.lower() != 'false':
                response_payload[timezone]['elements'] = {
                    'date': {
                        'day': {
                            'weekday': {
                                'full': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%A'
                                ),
                                'abbreviated': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%a'
                                ),
                                'number': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%w'
                                )
                            },

                            'day_of_month_zero_padded': datetime.datetime.strftime(
                                addition_in_tz,
                                '%d'
                            ),
                            'day_of_month_non_zero_padded': datetime.datetime.strftime(
                                addition_in_tz,
                                '%-d'
                            ),

                            'day_of_year': addition_in_tz.day_of_year

                        },

                        'week': {
                            'week_of_year': addition_in_tz.isocalendar()[1],
                            'week_of_month': addition_in_tz.week_of_month
                        },

                        'month': {
                            'full_name': datetime.datetime.strftime(
                                addition_in_tz,
                                '%B'
                            ),
                            'abbreviated_name': datetime.datetime.strftime(
                                addition_in_tz,
                                '%b'
                            ),
                            'day_of_month_zero_padded': datetime.datetime.strftime(
                                addition_in_tz,
                                '%d'
                            ),
                            'day_of_month_non_zero_padded': datetime.datetime.strftime(
                                addition_in_tz,
                                '%-d'
                            )
                        },
                        'year': {
                            'without_century': datetime.datetime.strftime(
                                addition_in_tz,
                                '%y'
                            ),
                            'with_century': datetime.datetime.strftime(
                                addition_in_tz,
                                '%Y'
                            )
                        },

                        'quarter': addition_in_tz.quarter
                    },

                    'time': {
                        '24_hour': {
                            'hour': {
                                'zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%H'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%-H'
                                )
                            },
                            'minute': {
                                'zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%M'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%-M'
                                )
                            },
                            'second': {
                                'zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%S'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%S'
                                )
                            },
                            'milisecond': datetime.datetime.strftime(
                                addition_in_tz,
                                '%f'
                            )

                        },

                        '12_hour': {
                            'hour': {
                                'zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%I'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%-I'
                                )
                            },

                            'minute': {
                                'zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%M'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%-M'
                                )
                            },

                            'second': {
                                'zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%S'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    addition_in_tz,
                                    '%S'
                                )
                            },

                            'milisecond': datetime.datetime.strftime(
                                addition_in_tz,
                                '%f'
                            ),

                            'am_pm': datetime.datetime.strftime(
                                addition_in_tz,
                                '%p'
                            ),
                        },
                        'timezone': addition_in_tz.timezone_name
                    },

                    'timezone_offset': datetime.datetime.strftime(
                        addition_in_tz,
                        '%z'
                    )
                }

    try:
        if len(timezones) < len(request.get_json()['timezones']):
            response_payload['errors'] = 'At least one invalid timezone passed in the request.'

    except:
        pass

    return {
        'status': 'Success',
        'converted_data': response_payload
    }
