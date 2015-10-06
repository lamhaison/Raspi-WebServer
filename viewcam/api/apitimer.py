
from datetime import datetime, timedelta

import logging
logger = logging.getLogger(__name__)


def get_now_time_without_second():

    """
    :return: return now time that have is not second unit.
    """
    try:
        now_time = datetime.now()
        now_time = datetime(now_time.year, now_time.month, now_time.day, now_time.hour, now_time.minute)

        return now_time
    except Exception as ex:
        logger.debug(ex)
        return None


def get_now_time_with_second():
    try:
        now_time = datetime.now()
        now_time = datetime(now_time.year, now_time.month, now_time.day, now_time.hour, now_time.minute, now_time.second)
        return now_time
    except Exception as ex:
        logger.debug(ex)
        return None


# Get now time with full unit time
def get_full_unit_now_time():
    try:
        now_time = datetime.now()
        return now_time
    except Exception as ex:
        logger.debug(ex)
        return None


def get_time_with_format(formatTime):
    """
    :param formatTime: specified format
    :return:time string
    """
    try:

        return datetime.now().strftime(formatTime)
    except Exception as ex:
        logger.debug(ex)
        return None


def get_time_with_format_from_time(format_time, time_object):
    """
    :param formatTime: specified format
    :param time_object: object time do you want to convert to string with format
    :return:time string
    """
    try:

        return time_object.strftime(format_time)
    except Exception as ex:
        logger.debug(ex)
        return None

def get_real_time():
    """
    :return: get now time that have a format
    """
    try:

        return datetime.now().strftime("%H:%M:%S")
    except Exception as ex:
        logger.debug(ex)
        return None


def get_string_time(time_obj):
    """
    :param time_obj: time object
    :return: chang time to string to view on graph
    """
    return time_obj.strftime("%H:%M")


def get_interval(now_time, alarm_time):
    """
    Get interval time between two time point
    :param now_time: this is now time
    :param alarm_time: this is When device will be turn on or turn off
    :return: show string, which will view interval. Such as 2Day4h10
    """

    if now_time is None or alarm_time is None:
        return None

    if alarm_time <= now_time:
        return None

    interval = alarm_time - now_time
    interval_second = interval.seconds
    interval_day = interval.days
    interval_minute = 0
    interval_hour = 0

    time_string = ""

    # Get date
    if interval_day > 0:
        time_string = "%sDay" % interval_day

        # Get total second time after calculate how many date
        interval_second = (interval_second % 86400)

    # If total second is bigger than one hour
    if interval_second > 3600:
        # Calculate how many hour
        interval_hour = int(interval_second / 3600)

        # Get remain total second
        interval_second = (interval_second % 3600)
        if interval_second > 0:
            interval_minute = int(interval_second / 60)

            # Remain second will be calculate to next minute
            if (interval_second % 60) > 0:
                interval_minute = (interval_minute + 1)
            time_string = "%s%sH%sM" % (time_string, interval_hour, interval_minute)
        else:
            time_string = "%s%sH" % (time_string, interval_hour)
    else:

        interval_minute = int(interval_second / 60)

        # Remain second will be calculate to next minute
        if (interval_second % 60) > 0:
            interval_minute = (interval_minute + 1)

        if interval_minute > 0:
            time_string = "%s%sM" % (time_string, interval_minute)

    return time_string


def get_alarm_time(year, month, date, hour, minute):
    """
    :param year: year of date of alarm time
    :param month: month of date of alarm time
    :param date: date of date of alarm time
    :param hour: alarm hour
    :param minute: alarm minute
    :return: alarm time that have year, month, .... equal input data
    """
    try:
        time = datetime(int(year), int(month), int(date), int(hour), int(minute))
        return time
    except Exception as ex:
        logger.debug(ex)
        return None


def get_alarm_time_from_specified_hour_minute(hour, minute):
    """
    :param hour: alarm hour
    :param minute: alarm minute
    :return:
    """
    now_time = get_now_time_without_second()
    try:
        alarm_time = now_time + timedelta(hours=hour, minutes=minute)
        return alarm_time
    except Exception as ex:
        logger.debug(ex)
        return None
