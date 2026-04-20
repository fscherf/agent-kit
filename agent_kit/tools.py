import datetime


def get_current_time():
    """
    Returns the current time as an ISO string.
    """

    return str(datetime.datetime.now().isoformat())


def get_default_tools():
    return [
        get_current_time,
    ]
