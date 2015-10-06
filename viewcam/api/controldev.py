__author__ = 'root'

import commands
import logging
import videoapi
import accessdb
from random import randint
from viewcam.api import apitimer
from django.conf import settings
logger = logging.getLogger(__name__)




def get_alert_fire_status():
    """
    :return: get status of sound fire. If 0 is off, 1 is on
    """
    command = 'gpio read %s' % '27'
    # logger.debug(command)
    status = 'OFF'
    try:
        result = commands.getoutput(command)
        status = 'OFF'
        # logger.debug(result)
        if result == '1':
            status = 'ON'
        return status
    except Exception as ex:
        logger.error(ex)
        return status


def control_alert_fire(action):
    """
    :param action: int type, on or off. if on, action is 1, if off, action is 0
    :return:
    """
    status = get_alert_fire_status()
    if status == 'ON' and action == 1:
        logger.debug('Can not start device again')
        return False

    if status == 'OFF' and action == 0:
        logger.debug('Can not off device again')
        return False

    try:
        query = 'gpio write %s %s' % ('27', action)
        result = commands.getoutput(query)
        # logger.debug(result)
        return True
    except Exception as ex:
        logger.error(ex)
        return False



def get_temp():
    """
    :return: return now temperature by return data type is float
    """
    command = "cat /sys/bus/w1/devices/28-00043e11a5ff/w1_slave | grep 't=' | awk -F 't=' {'print$2'}"
    try:
        result = commands.getoutput(command)
#        logger.debug(result)
        now_temp = float(result)
        now_temp = float(now_temp / 1000)
        now_temp = float("{0:.2f}".format(now_temp))

    except Exception as detail:
        logger.error(detail)
        now_temp = randint(20,50)
        now_temp = value = float("{0:.2f}".format(now_temp))

    return now_temp


def get_all_device_status():

    """
    :return: Get all status of all device, return a hash list with key is a device name
    """

    status_list = {}
    dev_list = accessdb.get_device_list()
    for row in dev_list:
        # logger.debug(row.id)
        key = 'dev%s' % row.id
        result = get_device_status(row.id)
        status_list[key] = result

    return status_list


def update_device_status_interval():
    dev_list = accessdb.get_device_list()
    for row in dev_list:
        result = get_device_status(row.id)
        if result != row.status:
            update_status_device(row, result)


def get_device_status(dev):

    """
    :param dev:is device id. Such as 1 have device name is dev1
    :return: device status. If device is 0 then status is OFF and device is 1 then status is ON
    """
    command = 'gpio read %s' % dev
    result = commands.getoutput(command)
    status = 'OFF'
    if result == '0':
        status = 'ON'

    return status


def get_device_status_to_code(dev):

    """
    :param dev:is device id. Such as 1 have device name is dev1
    :return: device status. If device is 0 then status return is 0 and device is 1 then status is 1
    """
    command = 'gpio read %s' % dev
    result = commands.getoutput(command)

    try:
        code = int(result)
    except Exception as ex:
        logger.debug(ex)
        return 0

    return code


def control_device(dev, action):
    """
    :param dev: device is such as 1 have device name is dev1
    :param action: this is a specified action such as 0 is turn off device, 1 is turn on device
    :return: device status after action have been performed success.
    """

    status = get_device_status(dev)
    if status == 'ON':
        if action == 0:
            msg = 'device %s have status ON. Can not open again. Please check information' % dev
            logger.debug(msg)
            return get_device_status(dev)
    if status == 'OFF':
        if action == 1:
            msg = 'device %s have status OFF. Can not close again. Please check information' % dev
            logger.debug(msg)
            return get_device_status(dev)
    try:

        command = 'gpio write %s %s' % (dev, action)
        commands.getoutput(command)
    except Exception as ex:
        logger.debug(ex)

    status = get_device_status(dev)
    update_status_device(dev, status)

    return status


# Update status device on database
def update_status_device(dev, status):
    msg = 'check status device %s' % dev
    logger.debug(msg)

    # Check status device have been chang. If true insert history and update device status on device table
    accessdb.check_change_dev_status_using_key(dev, status)


def change_status_to_code(status):
    if status == "ON" or status == 'on':
        return 1
    else:
        return 0


# Check exist raspivid process
def check_exist_raspivid_process():
    query = "ps -ef |grep raspivid | grep -v 'grep raspivid'"
    result = commands.getoutput(query)
    # logger.debug(result)
    if result != '':
        return True
    return False


# Write video to file without streaming
def run_raspivid_process_without_streaming():


    file_name = videoapi.get_name_video(settings.EXTENSION_VIDEO_FILE)
    file_name = '%s/%s' % (settings.VIDEO_DIR, file_name)
    query = 'raspivid -t 0 -w 960 -h 540 -fps 25 -b 500000 -vf -o %s' % file_name
    # logger.debug(query)
    logger.debug(query)
    result = commands.getoutput(query)


# Get command run video to file without streaming
def get_command_run_raspivid_process_without_streaming():
    file_name = videoapi.get_name_video(settings.EXTENSION_VIDEO_FILE)
    file_name = '%s/%s' % (settings.VIDEO_DIR, file_name)
    query = 'raspivid -t 0 -w 960 -h 540 -fps 25 -b 500000 -vf -o %s' % file_name
    logger.debug(query)
    return query


def get_status_camera():
    """
    Get status of camera device. On, off
    :return:
    """

    command = 'ps -ef| grep "0.0.0.0:6666" | grep -v "grep 0.0.0.0:6666"'
    try:
        result = commands.getoutput(command)
        if result == "":
            return 'off'
        else:
            return 'on'
    except Exception as ex:
        logger.debug(ex)
        return 'off'


def control_camera(action):
    """
    :param action: specified action such as down, up, left, right, stop, start
    :return: result of operation
    """

    msg = 'action with cam: %s' % action
    logger.debug(msg)
    try:

        if action == 'stop':
            result = commands.getoutput('pkill -9 raspivid')
            logger.debug(result)
            return True
        elif action == 'start':
            result = commands.getoutput('pkill -9 raspivid')
            file_name = videoapi.get_name_video(settings.EXTENSION_VIDEO_FILE)
            path = settings.VIDEO_DIR
            # logger.debug(path)
            file_name = '%s/%s' % (path, file_name)
            # logger.debug(file_name)


            default_detail = videoapi.get_all_default_value()
            if default_detail is None:
                logger.error('Can get default detail of value')
                return False
            fps = default_detail[settings.VIDEO_TYPE_OPTION[1][0]]
            h = default_detail[settings.VIDEO_TYPE_OPTION[2][0]]['h']
            w = default_detail[settings.VIDEO_TYPE_OPTION[2][0]]['w']
            bit_rate = default_detail[settings.VIDEO_TYPE_OPTION[0][0]]

            command = '/usr/bin/raspivid -t 0 -w %s -h %s -fps %s -b %s -vf -o -| tee %s | /usr/local/bin/ffmpeg -i - ' \
                      '-vcodec copy -an -f flv -metadata streamName=myStream tcp://0.0.0.0:6666' % \
                      (w, h, fps, bit_rate, file_name)

            logger.debug(command)
            result = commands.getoutput(command)
            logger.debug(result)
            return True
        elif action == 'left' or action == 'down' or action == 'up' or action == 'right':
            control_cam_path = settings.CONTROL_CAM_PATH
            command = '%s/%s' % (control_cam_path, action)
            result = commands.getoutput(command)
            result = commands.getoutput(command)
            result = commands.getoutput(command)
            result = commands.getoutput(command)
            result = commands.getoutput(command)
            logger.debug(result)
            # Success to perform action
            if result == '':
                return True

        return False
    except Exception as detail:
        logger.debug(detail)
        return False


def run_cam_with_special_property(command):
    """
    Run cam with some option from user
    :param command: command run cam with some param
    :return:
    """

    try:
        # Turn off cam
        cam_status = get_status_camera()

        # Cam turn on
        if cam_status == 'on':
            result = control_camera('stop')
            logger.debug(result)

            #Can't stop cam
            if result is False:
                return False

        # Turn on cam with some param
        result = commands.getoutput(command)
        return True
    except Exception as ex:
        logger.debug(ex)
        return False

