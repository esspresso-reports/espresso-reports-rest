from datetime import datetime


def string_to_date(date_string: str):
    return datetime.strptime(date_string, '%Y-%m-%d').date()


def string_to_datetime(date_string: str):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ').date()
