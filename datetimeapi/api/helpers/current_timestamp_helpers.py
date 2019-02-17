from flask import request
import pendulum
import datetime


def prepare_current_timestamp_response():
    timezones = request.args.getlist("tz")
    elements = request.args.get('elements')
    only_elements = request.args.get('only_elements')
    now_utc = pendulum.now("UTC")
    response_payload = {
        'UTC': {

        }
    }

    if not only_elements or only_elements.lower() != 'true':
        response_payload['UTC'] = {
            'timezone_aware': str(now_utc),
            'iso_8601_format': now_utc.to_iso8601_string(),
            'atom': now_utc.to_atom_string(),
            'cookie': now_utc.to_cookie_string(),
            'rss': now_utc.to_rss_string(),
            'w3c': now_utc.to_w3c_string(),
            'datetime': {
                'datetime_string': now_utc.to_datetime_string(),
                'date_string': now_utc.to_date_string(),
                'time_string': now_utc.to_time_string()
            },

            'rfc': {
                'rfc822': now_utc.to_rfc822_string(),
                'rfc850': now_utc.to_rfc850_string(),
                'rfc1036': now_utc.to_rfc1036_string(),
                'rfc1123': now_utc.to_rfc1123_string(),
                'rfc2822': now_utc.to_rfc2822_string(),
                'rfc3339': now_utc.to_rfc3339_string()
            },

            'epoch': {
                'float': now_utc.float_timestamp,
                'integer': now_utc.int_timestamp
            },

            'pretty': {
                '12_hour': datetime.datetime.strftime(
                    now_utc,
                    '%D %-I:%M %p'
                ),
                '24_hour': datetime.datetime.strftime(
                    now_utc,
                    '%D %H:%M'
                )
            },

            'descriptive': {
                '12_hour': datetime.datetime.strftime(
                    now_utc,
                    '%A, %B %-d, %Y %-I:%M %p'
                ),
                '24_hour': datetime.datetime.strftime(
                    now_utc,
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
                            now_utc,
                            '%A'
                        ),
                        'abbreviated': datetime.datetime.strftime(
                            now_utc,
                            '%a'
                        ),
                        'number': datetime.datetime.strftime(
                            now_utc,
                            '%w'
                        )
                    },

                    'day_of_month_zero_padded': datetime.datetime.strftime(
                        now_utc,
                        '%d'
                    ),
                    'day_of_month_non_zero_padded': datetime.datetime.strftime(
                        now_utc,
                        '%-d'
                    ),

                    'day_of_year': now_utc.day_of_year

                },

                'week': {
                    'week_of_year': now_utc.isocalendar()[1],
                    'week_of_month': now_utc.week_of_month
                },

                'month': {
                    'full_name': datetime.datetime.strftime(
                        now_utc,
                        '%B'
                    ),
                    'abbreviated_name': datetime.datetime.strftime(
                        now_utc,
                        '%b'
                    )
                },

                'year': {
                    'without_century': datetime.datetime.strftime(
                        now_utc,
                        '%y'
                    ),
                    'with_century': datetime.datetime.strftime(
                        now_utc,
                        '%Y'
                    )
                },

                'quarter': now_utc.quarter
            },

            'time': {
                '24_hour': {
                    'hour': {
                        'zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%H'
                        ),
                        'non_zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%-H'
                        )
                    },
                    'minute': {
                        'zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%M'
                        ),
                        'non_zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%-M'
                        )
                    },
                    'second': {
                        'zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%S'
                        ),
                        'non_zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%S'
                        )
                    },
                    'milisecond': datetime.datetime.strftime(
                        now_utc,
                        '%f'
                    )

                },

                '12_hour': {
                    'hour': {
                        'zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%I'
                        ),
                        'non_zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%-I'
                        )
                    },

                    'minute': {
                        'zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%M'
                        ),
                        'non_zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%-M'
                        )
                    },

                    'second': {
                        'zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%S'
                        ),
                        'non_zero_padded': datetime.datetime.strftime(
                            now_utc,
                            '%S'
                        )
                    },

                    'milisecond': datetime.datetime.strftime(
                        now_utc,
                        '%f'
                    ),

                    'am_pm': datetime.datetime.strftime(
                        now_utc,
                        '%p'
                    ),
                },
                'timezone': now_utc.timezone_name
            },

            'timezone_offset': datetime.datetime.strftime(
                now_utc,
                '%z'
            )
        }

    valid_timezones = []

    if timezones:
        for timezone in timezones:
            try:
                time_zone_now = now_utc.in_timezone(timezone)
                valid_timezones.append(timezone)

            except:
                response_payload['errors'] = """At least one invalid timezone passed as a parameter."""

    if timezones:
        for timezone in valid_timezones:
            time_zone_now = now_utc.in_timezone(timezone)

            if not only_elements or only_elements.lower() != 'true':
                response_payload[timezone] = {
                    'timezone_aware': str(time_zone_now),
                    'iso_8601_format': time_zone_now.to_iso8601_string(),
                    'atom': time_zone_now.to_atom_string(),
                    'cookie': time_zone_now.to_cookie_string(),
                    'rss': time_zone_now.to_rss_string(),
                    'w3c': time_zone_now.to_w3c_string(),
                    'datetime': {
                        'datetime_string': time_zone_now.to_datetime_string(),
                        'date_string': time_zone_now.to_date_string(),
                        'time_string': time_zone_now.to_time_string()
                    },

                    'rfc': {
                        'rfc822': time_zone_now.to_rfc822_string(),
                        'rfc850': time_zone_now.to_rfc850_string(),
                        'rfc1036': time_zone_now.to_rfc1036_string(),
                        'rfc1123': time_zone_now.to_rfc1123_string(),
                        'rfc2822': time_zone_now.to_rfc2822_string(),
                        'rfc3339': time_zone_now.to_rfc3339_string()
                    },

                    'epoch': {
                        'float': time_zone_now.float_timestamp,
                        'integer': time_zone_now.int_timestamp
                    },

                    'pretty': {
                        '12_hour': datetime.datetime.strftime(
                            time_zone_now,
                            '%D %-I:%M %p'
                        ),
                        '24_hour': datetime.datetime.strftime(
                            time_zone_now,
                            '%D %H:%M'
                        )
                    },

                    'descriptive': {
                        '12_hour': datetime.datetime.strftime(
                            time_zone_now,
                            '%A, %B %-d, %Y %-I:%M %p'
                        ),
                        '24_hour': datetime.datetime.strftime(
                            time_zone_now,
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
                                    time_zone_now,
                                    '%A'
                                ),
                                'abbreviated': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%a'
                                ),
                                'number': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%w'
                                )
                            },

                            'day_of_month_zero_padded': datetime.datetime.strftime(
                                time_zone_now,
                                '%d'
                            ),
                            'day_of_month_non_zero_padded': datetime.datetime.strftime(
                                time_zone_now,
                                '%-d'
                            ),

                            'day_of_year': time_zone_now.day_of_year

                        },

                        'week': {
                            'week_of_year': time_zone_now.isocalendar()[1],
                            'week_of_month': time_zone_now.week_of_month
                        },

                        'month': {
                            'full_name': datetime.datetime.strftime(
                                time_zone_now,
                                '%B'
                            ),
                            'abbreviated_name': datetime.datetime.strftime(
                                time_zone_now,
                                '%b'
                            ),
                            'day_of_month_zero_padded': datetime.datetime.strftime(
                                time_zone_now,
                                '%d'
                            ),
                            'day_of_month_non_zero_padded': datetime.datetime.strftime(
                                time_zone_now,
                                '%-d'
                            )
                        },
                        'year': {
                            'without_century': datetime.datetime.strftime(
                                time_zone_now,
                                '%y'
                            ),
                            'with_century': datetime.datetime.strftime(
                                time_zone_now,
                                '%Y'
                            )
                        },

                        'quarter': time_zone_now.quarter
                    },

                    'time': {
                        '24_hour': {
                            'hour': {
                                'zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%H'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%-H'
                                )
                            },
                            'minute': {
                                'zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%M'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%-M'
                                )
                            },
                            'second': {
                                'zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%S'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%S'
                                )
                            },
                            'milisecond': datetime.datetime.strftime(
                                time_zone_now,
                                '%f'
                            )

                        },

                        '12_hour': {
                            'hour': {
                                'zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%I'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%-I'
                                )
                            },

                            'minute': {
                                'zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%M'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%-M'
                                )
                            },

                            'second': {
                                'zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%S'
                                ),
                                'non_zero_padded': datetime.datetime.strftime(
                                    time_zone_now,
                                    '%S'
                                )
                            },

                            'milisecond': datetime.datetime.strftime(
                                time_zone_now,
                                '%f'
                            ),

                            'am_pm': datetime.datetime.strftime(
                                time_zone_now,
                                '%p'
                            ),
                        },
                        'timezone': time_zone_now.timezone_name
                    },

                    'timezone_offset': datetime.datetime.strftime(
                        time_zone_now,
                        '%z'
                    )
                }

    return response_payload
