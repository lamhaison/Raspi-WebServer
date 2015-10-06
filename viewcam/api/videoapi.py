__author__ = 'root'
import apitimer
import commands
import os
from datetime import datetime, timedelta
import controldev, accessdb

import logging
logger = logging.getLogger(__name__)
from django.conf import settings




def get_name_video(extension):
    """
    Get name using now time + extension file. Ex: .mp4
    :return: Name file from now time
    """
    time_string = apitimer.get_time_with_format("%Y-%m-%d-%H-%M-%S")
    name_file = '%s.%s' % (time_string, extension)
    logger.debug(name_file)
    # command = 'touch /var/www/video/%s' % name_file
    # logger.debug(command)
    # result = commands.getoutput(command)
    # logger.debug(result)

    return name_file


def get_list_video():
    """
    Get list file in path /var/www/video
    :return:
    """
    path_video = settings.VIDEO_DIR
    logger.debug(path_video)
    extension = settings.EXTENSION_VIDEO_FILE
    command = "ls %s -lrt | grep '%s' | grep -v 'total' | awk '{print$9}'" % (path_video, extension)
    # logger.debug(command)
    pipe = os.popen(command)
    result = pipe.read().strip().split()
    logger.debug(result)
    # logger.debug(result)

    return result


def get_created_time_of_file(file_name):
    """
    :param namefile: name file do you want to get created time
    :return: datetime for created file
    """

    name_split = file_name.split('.')
    # Get name of file, reverse file extension
    time_string = name_split[0]
    # logger.debug(time_string)

    time_split = time_string.split('-')
    # logger.debug(time_split)

    create_time = apitimer.get_alarm_time(time_split[0], time_split[1], time_split[2], time_split[3], time_split[4])

    return create_time


def check_true_time(now_time, interval, file_name):
    """
    :param now_time: now time at the check time
    :param interval: such as 1h, 5m, 2h
    :return: if created time of file is between now_time, now_time - interval, the return true, or return false
    """
    pre_time = now_time - timedelta(minutes=interval)
    # logger.debug(file_name)

    created_time = get_created_time_of_file(file_name)
    # logger.debug(now_time)
    # logger.debug(created_time)
    # logger.debug(pre_time)
    if created_time >= pre_time:
        if created_time < now_time:
            return True

    return False


def convert_h264_to_mp4(file_name):
    """
    :param file_name: name of file
    :return: return True if success otherwise return False
    """

    path = settings.VIDEO_DIR
    try:
        name_split = file_name.split('.')
        # logger.debug(name_split[0])
        # Name is not have extension file
        name = name_split[0]
        mp4_name = '%s/%s.mp4' % (path, name)
        # logger.debug(mp4_name)
        command = '/usr/local/bin/ffmpeg -i %s/%s -vcodec copy %s' % (path, file_name, mp4_name)
        result = commands.getoutput(command)
        logger.debug(command)
        logger.debug(result)

        return True
    except Exception as ex:
        logger.debug(ex)
        return False


# Run function using crontab
def run_using_crontab():
    result_list = get_list_video()
    # Remmove video
    result_list.pop(len(result_list) - 1)
    logger.debug(result_list)
    # controldev.control_camera('stop')
    # controldev.control_camera('start')
    # now_time = apitimer.get_now_time_with_second()
    # logger.debug(now_time)
    for row in result_list:
        ret = convert_h264_to_mp4(row)
        if ret:
            command = 'rm -rf %s/%s' % (settings.VIDEO_DIR, row)
            logger.debug(command)
            result = commands.getoutput(command)
            logger.debug(result)

            msg = 'convert %s: %s' % (row, ret)
            logger.debug(msg)
        # logger.debug(row)
        # ret = check_true_time(now_time, int(settings.INTERVAL_VIDEO), row)
        # logger.debug(ret)

# Get size from format such as 220x470: w: 220, h: 470
def get_size(size_format):
    """
    :param size_format: format of video's size
    :return: dict have structure:
        {
            'w': 220
            'h': 470
        }
    """

    if size_format is None:
        logger.error('size format is None')
        return None

    size_detail = {}
    try:
        px_split = size_format.split('x')
        size_detail['h'] = px_split[1]
        size_detail['w'] = px_split[0]

        return size_detail
    except Exception as ex:
        logger.error(ex)
        return None


def get_all_default_value():

    """
    :return:dict have structure:
    {
        'bitrate': 'integer'
        'fps': 'integer'
        'size': {
            'h': integer
            'w': integer
        }
    }
    """
    fps = accessdb.get_default_value_specified_type(settings.VIDEO_TYPE_OPTION[1][0])
    if fps is None:
        logger.error('Can not get fps default')
        return None
    bit_rate = accessdb.get_default_value_specified_type((settings.VIDEO_TYPE_OPTION[0][0]))
    if bit_rate is None:
        logger.error('Can not get bitrate default')
        return None

    size = accessdb.get_default_value_specified_type(settings.VIDEO_TYPE_OPTION[2][0])
    if size is None:
        logger.error('Can not get size default')
        return None
    try:

        detail = {}
        detail[settings.VIDEO_TYPE_OPTION[1][0]] = fps.value
        detail[settings.VIDEO_TYPE_OPTION[0][0]] = bit_rate.value

        detail_size = get_size(size.value)
        if detail_size is None:
            logger.error('Can not parse size format')
            return None
        detail[settings.VIDEO_TYPE_OPTION[2][0]] = detail_size

        return detail
    except Exception as ex:
        logger.error(ex)
        return None


















