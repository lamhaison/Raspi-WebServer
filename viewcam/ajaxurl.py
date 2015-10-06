from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django_ajax.decorators import ajax
from django.utils import timezone
import json
from api import controldev
from api import accessdb
from api import apitimer, videoapi
from datetime import datetime, timedelta
import random
from django.conf import settings


from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger(__name__)


@ajax
def get_time(request):
    """
    :param request:  request html
    :return: now time by return json
    """

    now_time = apitimer.get_real_time()

    return HttpResponse(json.dumps({"time": now_time}), content_type="application/json")


@ajax
def get_temp(request):
    """
    :param request: request html
    :return: now temperature by return json
    """
    temp_float = controldev.get_temp()
    return HttpResponse(json.dumps({"temp": temp_float}),
            content_type="application/json")

@ajax
# Get nowTime and temp
def get_info(request):
    # Get temp
    # logger.debug(apitimer.get_full_unit_now_time())
    temp_float = controldev.get_temp()
    status_list = controldev.get_all_device_status()
    # logger.debug(apitimer.get_full_unit_now_time())
    now_time = apitimer.get_real_time()
    # Return json
    return HttpResponse(json.dumps({'time': now_time, 'temp': temp_float, 'dev': status_list}),
                        content_type="application/json")


@ajax
def control_device(request, device_id, action_id):
    status = controldev.control_device(device_id, action_id)
    return HttpResponse(json.dumps({'dev': device_id, 'status': status}), content_type='application/json')


@ajax
# Get all status of device
def get_all_status(request):

    status_list = controldev.get_all_device_status()
    return HttpResponse(json.dumps(status_list), content_type='application/json')


@ajax
def get_device_status(request, device_id):
    status = controldev.get_device_status(device_id)
    return HttpResponse(json.dumps({'dev': device_id, 'status': status}), content_type='application/json')


# Return json with error message. message will make following code
def return_json(code):
    if code:
        return HttpResponse(json.dumps({'status': True, 'msg': 'ok'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': False, 'msg': 'Fail'}), content_type='application/json')


# Set action alarm by time from user
def set_alarm_time(device_id, timer, action, alarm_time):

    if action == 'on' or action == 'off':

        # Get alertTime
        alarm_record = accessdb.get_specified_alarm_time(device_id, timer)
        # alarm time is not exist. Create a new alarm time record
        if alarm_record is None:

            # Get device
            dev = accessdb.get_device_from_pk(device_id)
            # Device is not exist. Create new device
            if dev is None:
                dev_name = "dev%s" % device_id
                dev = accessdb.create_device(dev_name, '')
                # Can't create device
                if dev is None:
                    return False
            alarm_record = accessdb.create_alarm_using_time(dev, action, alarm_time, timer)
            # Check create alarm time record
            if alarm_record is None:
                return False
            else:
                return True

        else:
            # Have exist alarm time
            result = accessdb.enable_alarm_time(device_id, action, alarm_time, timer)
            return result

    # Action is removed
    if action == 'remove':
        result = accessdb.disable_alarm_time(device_id, timer)
        return result

    # Can't known this action
    return False


@ajax
def remove_alarm_by_time(request, device_id, timer):
    result = accessdb.disable_alarm_time(device_id, timer)
    return return_json(result)


@ajax
def alarm_by_date(request, device_id, timer, action, day, month, year, hour, minute):

    now_time = apitimer.get_now_time_without_second()
    alarm_time = apitimer.get_alarm_time(int(year), int(month), int(day), int(hour), int(minute))

    # Have error when get time
    if alarm_time is None or now_time is None:
        return return_json(False)

    # AlertTime not pass to valid
    if now_time > alarm_time:
        return False

    # Start process set alarm time record
    result = set_alarm_time(device_id, timer, action, alarm_time)

    return return_json(result)


@ajax
def alarm_by_minute(request, device_id, timer, action, minute):
    logger.debug('Go to alertMinute')
    now_time = apitimer.get_now_time_without_second()
    alarm_time = apitimer.get_alarm_time_from_specified_hour_minute(0, int(minute))

    # Have error when get time
    if alarm_time is None or now_time is None:
        return return_json(False)

    # Alarm Time not pass to valid
    if now_time > alarm_time:
        return False
    result = set_alarm_time(device_id, timer, action, alarm_time)
    return return_json(result)


@ajax
def remove_alarm_by_temp(request, device_id):
    ret = accessdb.disable_alarm_by_temp(device_id)
    return return_json(ret)

@ajax
def get_alarm_by_temp(request, device_id):
    """
    :param request:
    :param device_id: device id
    :return: return detail of record alarm temp if this record is exist and have active is true
    """
    alarm_record = accessdb.get_alarm_by_temp(device_id)
    if alarm_record is None or alarm_record.active is False:
        return return_json(False)

    return HttpResponse(json.dumps({'status': True, 'dev': alarm_record.dev.id, 'condition': alarm_record.condition, 'action': alarm_record.action,
                                    'temp': alarm_record.value}), content_type='application/json')

@ajax
def get_all_alarm_by_temp(request):
    pass


@ajax
def alarm_by_temp(request, device_id, action, condition, value):
    print 'alarm by temp'
    # If action is remove alarm Condition
    dev = accessdb.get_device_from_pk(device_id)
    # Device is not exist
    if dev is None:
        dev_name = 'dev%s' % device_id
        dev = accessdb.create_device(dev_name, '')

        # Can't create new device
        if dev is None:
            return return_json(False)
        else:
            # Create new alarm
            alarm = accessdb.create_alarm_by_temp(dev, action, condition, value)
            if alarm is None:
                return return_json(False)

            return return_json(True)
    else:
        alarm = accessdb.get_alarm_by_temp(device_id)

        # Alarm condition is not exist
        if alarm is None:
            alarm = accessdb.create_alarm_by_temp(dev, action, condition, value)
            # Create alarm temp is not successful
            if alarm is None:
                return return_json(False)
            else:
                # Create successful
                return return_json(True)
        else:
            # Enable alarm condition
            ret = accessdb.enable_alarm_by_temp(device_id, condition, action, value)
            return return_json(ret)


@ajax
def get_alarm_by_time(request, device_id, timer):

    alarm_record = accessdb.get_specified_alarm_time(device_id, timer)

    # If record is not exist, return false
    if alarm_record is None or alarm_record.active is False:
        return HttpResponse(json.dumps({'status': False, 'timer': timer, 'dev': device_id}),
                            content_type='application/json')

    now_time = apitimer.get_now_time_without_second()
    alarm_time = alarm_record.time

    time_string = apitimer.get_interval(now_time, alarm_time)
    # If have error have been happened
    if time_string is None:
        time_string = ""
    action = alarm_record.action
    return HttpResponse(json.dumps({'status': True, 'timer': timer, 'dev': device_id, 'action': action,
                                    'remain': time_string}), content_type='application/json')


@ajax
def get_all_alarm_by_time(request):
    dev_list = accessdb.get_device_list()
    if dev_list is None:
        return HttpResponse(json.dumps({'status': False}), content_type='application/json')

    info_list = {}
    for dev in dev_list:

        timer_list = accessdb.get_alarm_time_list_from_device_pk(dev.id)
        if timer_list is None:
            return HttpResponse(json.dumps({'status': False}), content_type='application/json')
        detail_alarm_list = {}
        for timer in timer_list:

            remain_time = None

            # Enable alarm time
            if timer.active:
                now_time = apitimer.get_now_time_without_second()
                remain_time = apitimer.get_interval(now_time, timer.time)

            action = timer.action
            if remain_time is None or remain_time == '':
                #print 'qua han, '
                remain_time = ''
                action = ''

            detail = {}

            detail['action'] = action
            detail['remain'] = remain_time

            key = 'timer%s' % timer.timer
            detail_alarm_list[key] = detail

        key = 'dev%s' % dev.id
        info_list[key] = detail_alarm_list

    return HttpResponse(json.dumps({'status': True, 'info': info_list}), content_type='application/json')


@ajax
def get_temp_list(request, interval, unit):

    interval_time = 30
    type = '1min'

    if unit == 'min':
        type = '%s%s' % (interval, 'm')
        interval_time = interval_time * int(interval)
    elif unit == 'hour':
        type = '%s%s' % (interval, 'h')
        interval_time = interval_time * int(interval) * 60
    elif unit == 'day':
        type = '%s%s' % (interval, 'd')
        interval_time = interval_time * int(interval) * 24 * 60

    # logger.debug(type)
    # logger.debug(interval_time)

    print interval, unit


    end_time = apitimer.get_now_time_without_second()
    start_time = end_time - timedelta(minutes=interval_time)
    temp_list = accessdb.get_temp_record_between_two_point_time(start_time, end_time, type)
    detail_temp_list = {}
    for record in temp_list:
        detail = {}
        detail['time'] = apitimer.get_string_time(record.time)
        detail['value'] = record.value

        detail_temp_list[record.id] = detail

    return HttpResponse(json.dumps({'status': True, 'temp_list': detail_temp_list}), content_type='application/json')


@ajax
def test_high_chart(request):

    nowTime = apitimer.get_now_time_without_second()
    string_time = apitimer.get_string_time(nowTime)
    value = random.randint(1, 100)

    return HttpResponse(json.dumps({'x': '', 'y': value}), content_type='application/json')


@ajax
def control_camera(request, action):
    """
    :param request: request of html
    :param action: specified action what you want to do with cam
    :return: json status : true is operated success, false is not success
    """

    # Cause get status of camera
    if action == 'status':
        result = controldev.get_status_camera()
        return HttpResponse(json.dumps({'status': True, 'cam_status': result}), content_type='application/json')

    # Turn on, off cam device
    if action == 'start' or action == 'stop':
        result = controldev.control_camera(action)

        status = controldev.get_status_camera()

        return HttpResponse(json.dumps({'status': result, 'cam_status': status}), content_type='application/json')


    result = controldev.control_camera(action)
    return return_json(result)


@ajax
def set_property_camera(request, px, bit_rate, frame_ps, sharpness, contrast, brightness, saturation, iso, ev, ex, awb):
    property_list = '%s %s %s %s %s %s %s %s %s %s %s ' % (px, bit_rate, frame_ps, sharpness, contrast, brightness,
                                                           saturation, iso, ev, ex, awb)

    try:

        # command = 'raspivid -t 0 -w 960 -h 540 -fps 25 -b 500000 -o -|ffmpeg -i - -vcodec copy -an -f flv -metadata streamName=myStream tcp://0.0.0.0:6666'

        command = '/usr/bin/raspivid -t 0'

        # Format is wxh
        height = '540'
        weight = '960'

        if px != 'none':
            px_parse = videoapi.get_size(px)
            if px_parse is not None:
                height = px_parse['h']
                weight = px_parse['w']

            logger.debug(height)
            logger.debug(weight)
        else:
            size = accessdb.get_default_value_specified_type(settings.VIDEO_TYPE_OPTION[2][0])
            if size is None:
                logger.error('Size default is not found')
                return return_json(False)
            detail_size = videoapi.get_size(size.value)
            if detail_size is None:
                logger.error('Do not parse size format')
                return return_json(False)

            height = detail_size['h']
            weight = detail_size['w']

        command = '%s -w %s -h %s -vf' % (command, weight, height)
        logger.debug(command)

        if frame_ps == 'none':
            frame_ps = accessdb.get_default_value_specified_type(settings.VIDEO_TYPE_OPTION[1][0])
            if frame_ps is None:
                logger.error('Can not ge frame ps default on database')
                return return_json(False)
            frame_ps = frame_ps.value


        if bit_rate == 'none':
            bit_rate = accessdb.get_default_value_specified_type(settings.VIDEO_TYPE_OPTION[0][0])
            if bit_rate is None:
                logger.error('Can not get bit rate default on database')
                return return_json(False)
            bit_rate = bit_rate.value

        command = '%s -fps %s -b %s' % (command, frame_ps, bit_rate)
        logger.debug(command)

        if sharpness != 'none':
            command = '%s -sh %s' % (command, sharpness)
            logger.debug(command)

        if contrast != 'none':
            command = '%s -co %s' % (command, contrast)
            logger.debug(command)

        if brightness != 'none':
            command = '%s -br %s' % (command, brightness)
            logger.debug(command)

        if saturation != 'none':
            command = '%s -sa %s' % (command, saturation)
            logger.debug(command)

        if iso != 'none':
            command = '%s -ISO %s' % (command, iso)
            logger.debug(command)

        if ev != 'none':
            command = '%s -ev %s' % (command, ev)
            logger.debug(command)

        if ex != 'none':
            command = '%s -ex %s' % (command, ex)
            logger.debug(command)

        if awb != 'none':
            command = '%s -awb %s' % (command, awb)
            logger.debug(command)


        # complete command
        file_name = videoapi.get_name_video(settings.EXTENSION_VIDEO_FILE)
        path = settings.VIDEO_DIR
        file_name = '%s/%s' % (path, file_name)
        logger.debug(file_name)
        end_command = '-o -| tee %s | ffmpeg -i - -vcodec copy -an -f flv ' \
                     '-metadata streamName=myStream tcp://0.0.0.0:6666' % file_name

        command = '%s %s' % (command, end_command)
        logger.debug(command)

        result = controldev.run_cam_with_special_property(command)
        return return_json(True)

    except Exception as ex:
        logger.debug(ex)
        return return_json(False)



# Create your views here.
