from flask import request
import pendulum

def get_difference():
    data = request.get_json()
    timestamp1 = data['timestamp1']

    try:
        valid_timestamp1 = pendulum.parse(timestamp1)

    except pendulum.parsing.exceptions.ParserError:
        return {
            'status': 'Failure',
            'error': 'Could not parse timestamp1 timestamp.'
        }

    except:
        return {
            'status': 'Failure',
            'error': 'Invalid or malformed timestamp2 timestamp.'
        }

    try:
        timestamp2 = data['timestamp2']

        try:
            valid_timestamp2 = pendulum.parse(timestamp2)

        except pendulum.parsing.exceptions.ParserError:
            return {
                'status': 'Failure',
                'error': 'Could not parse timestamp2 timestamp.'
            }

        except:
            return {
                'status': 'Failure',
                'error': 'Invalid or malformed timestamp2 timestamp.'
            }

    except KeyError:
        valid_timestamp2 = pendulum.now("UTC")

    difference = valid_timestamp1.diff(valid_timestamp2)
    
    return {
        'years': difference.in_years(),
        'months': difference.in_months(),
        'days': difference.in_days(),
        'weeks': difference.in_weeks(),
        'hours': difference.in_hours(),
        'minutes': difference.in_minutes(),
        'seconds': difference.in_seconds(),
        'human_readable': valid_timestamp1.diff_for_humans(
            valid_timestamp2, 
            absolute=True
        )
    }
