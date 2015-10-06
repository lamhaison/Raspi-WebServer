__author__ = 'root'
from viewcam.models import Device, Temperature, AlarmTemp, AlarmTime, DeviceHistory, VideoOption
from django.db.models import Q
from django.db import transaction
from django.db.models import Count, Avg
import logging
logger = logging.getLogger(__name__)
from django.conf import settings
import controldev
import apitimer



@transaction.atomic
def create_device(dev_name, desc):

    logger.debug('create device')
    """
    Create new device with nam device, and description for device
    :param dev_name:
    :param desc:
    :return: device that have been created
    """
    try:
        dev = Device(dev_name=dev_name, desc=desc)
        # Save dev into database successful
        dev.save()
        return dev
    # Can't create new device. Return None object
    except Exception as ex:
        logger.debug(ex)
        return None


def create_alarm_by_time_list_for_device(dev):

    logger.debug('create alarm by time')
    """
    :param dev: device object
    :return: not return
    """
    timer_list = settings.TIMER_LIST
    for timer in timer_list:
        create_alarm_using_time(dev, None, None, timer)
        disable_alarm_time(dev.id, timer)


def create_alarm_by_temp_for_device(dev):
    create_alarm_by_temp(dev, None, None, None)
    disable_alarm_by_temp(dev.id)


def get_device_list():

    """
    :return: get device list which include all device is exist on database
    """
    try:
        dev_list = Device.objects.all()
        return dev_list
    except Exception as ex:
        logger.debug(ex)
        return None


def get_device_from_name(dev_name):
    """
    :param dev_name: device name such as 'dev1' have device id is 1
    :return: Device. If device is not exist on database return None
    """
    try:
        dev = Device.objects.get(dev_name=dev_name)
        return dev
    except Exception as ex:
        logger.debug(ex)
        return None


def get_device_from_pk(dev_key):
    """
    :param dev_key: Key of device such as 1 have device name is dev1
    :return: Device. If device is not exist on database return None
    """

    try:
        dev = Device.objects.get(pk=dev_key)
        return dev
    except Exception as ex:
        logger.debug(ex)
        return None


def update_status_device_input_obj(dev, status):
    """
    :param dev_id: device object
    :param status: now status of device
    :return: True or False
    """
    try:
        if dev is None:
            logger.error('Can not get device')
            return False

        if dev.status == status:
            logger.error('Status in database equal input status')
            return False
        dev.status = status
        dev.save()
        return True
    except Exception as ex:
        logger.error(ex)
        return False


def update_status_device(dev_id, status):
    """
    :param dev_id: Device id
    :param status: now status of device
    :return: True or False
    """
    dev = get_device_from_pk(dev_id)
    if dev is None:
        logger.error('Can not get device')
        return False

    if dev.status == status:
        logger.error('Status in database equal input status')
        return False
    dev.status = status
    result = save(dev)
    return result


def check_change_dev_status_using_key(dev_id, now_status):
    """
    :param dev_id: id of device
    :param now_status: now status is True on, False: off
    :return: True or False. If status on db different with now_staus
    """
    try:
        dev = get_device_from_pk(dev_id)
        logger.debug(dev)
        # Can't get device
        if dev is None:
            return False

        # If status have been changed
        if dev.status != now_status:
            msg = 'status of dev %s to chang %s' % (dev_id, now_status)
            old_status = dev.status
            dev.status = now_status
            dev.save()

            ret = insert_history_device_status(dev, old_status, now_status)
            return ret

        return False
    except Exception as ex:
        logger.error(ex)
        return False


def check_change_dev_status_using_object(dev, now_status):
    """
    :param dev: Object device
    :param now_status:
    :return:
    """

    if dev is None:
        return False

    if dev.status != now_status:
        return True
    return False


def insert_history_device_status(dev, from_status, to_status):
    """
    status device from on to off
    :param dev: device object
    :param from_status: ex: True: on
    :param to_status: False: off
    :return: True if success, False is not success
    """
    try:
        now_time = apitimer.get_now_time_without_second()
        history_status = DeviceHistory(dev=dev, time=now_time, from_status=from_status, to_status=to_status)
        history_status.save()
        return True
    except Exception as ex:
        logger.error(ex)
        return False


def get_list_history_device_status(dev_id):
    """
    Get list history of device.
    :param dev_id: id of device
    :param max_record: maximun recored which you want to get
    :return: List record of status device which have id of dev_id
    """
    try:
        history_list = DeviceHistory.objects.filter(dev__id=dev_id)
        return history_list
    except Exception as ex:
        logger.error(ex)
        return None


def insert_history_device_status_using_device_key(dev_key, from_status, to_status):
    """
    status device from on to off
    :param dev: device key
    :param from_status: ex: True: on
    :param to_status: False: off
    :return: True if success, False is not success
    """
    try:
        now_time = apitimer.get_now_time_without_second()
        dev = get_device_from_pk(dev_key)
        if dev is None:
            return False

        history_status = DeviceHistory(dev=dev, time=now_time, from_status=from_status, to_status=to_status)
        history_status.save()
    except Exception as ex:
        logger.error(ex)
        return False



def create_alarm_using_time(dev, action, time, timer):
    """

    :param dev: Device object
    :param action: action will be perform when alarm time is expired such as on or off.
    :param time: time point alarm will be expired
    :param timer: sequence number of timer such as 1, 2, 3, 4
    :return: return alarm object that have just created on database
    """
    try:
        alarm_time = AlarmTime(dev=dev, action=action, time=time, timer=int(timer), active=True)
        alarm_time.save()
        return alarm_time
    except Exception as ex:
        logger.debug(ex)
        return None


def get_alarm_time(dev, timer):
    """
    :param dev: device object
    :param timer: sequence number of timer. Such as 1, 2, 3. 4
    :return: AlarmTime object
    """

    try:
        # Check the alarmTime is exist database
        alert_time = AlarmTime.objects.get(Q(dev=dev) & Q(timer=timer))
        return alert_time
    except Exception as ex:
        logger.debug(ex)
        # If is not exist
        return None


def enable_alarm_time(dev_id, action, time, timer):
    """
    Enable alertTime that is exist
    :param dev_id:
    :param action:
    :param time:
    :param timer:
    :return: True if enable success, False if enable is not success.
    """
    alert_time = get_specified_alarm_time(dev_id, timer)
    if alert_time is None:
        return False
    try:
        alert_time.active = True
        alert_time.action = action
        alert_time.time = time
        alert_time.timer = timer
        alert_time.save()

        return True
    except Exception as ex:
        logger.debug(ex)
        return False


# Disable a alarm time
def disable_alarm_time(dev_id, timer):
    """
    :param dev_id: device id such as 1 have device name is dev1
    :param timer: sequence timer such as 1, 2, 3. ...
    :return: True if perform success, otherwise return False.
    """
    try:

        alert_time = get_specified_alarm_time(dev_id, timer)

        # Alarm Record is not exist
        if alert_time is None or alert_time.active is False:
            return False

        # Disable alarm
        alert_time.active = False
        alert_time.action = None
        alert_time.time = None
        alert_time.save()

        return True
    except Exception as ex:
        logger.debug(ex)
        return False


def get_alarm_time_list():
    """
    :return: Get all alarm time in AlertTime table on database.
    """
    try:
        alert_list = AlarmTime.objects.filter().order_by('id')
        return alert_list
    except Exception as ex:
        logger.debug(ex)
        return None


# Get object from device name
def get_alarm_time_list_from_device_name(dev_name):
    """
    :param dev_name: such as dev1, dev2...
    :return: alarm list of device_name
    """
    try:
        alarm_time = AlarmTime.objects.filter(dev__dev_name=dev_name)
        return alarm_time
    except Exception as ex:
        logger.debug(ex)
        return None


# Get object from device key
def get_alarm_time_list_from_device_pk(dev_id):
    try:
        alert_time = AlarmTime.objects.filter(dev__id=dev_id).order_by('timer')
        return alert_time
    except Exception as ex:
        logger.debug(ex)
        return None


# Get enabled AlarmTime List
def get_enabled_alarm_time_list():
    try:
        alert_list = AlarmTime.objects.filter(active=True)
        return alert_list
    except Exception as ex:
        logger.debug(ex)
        return None


# Get specify alertTimer with dev_id and timer
def get_specified_alarm_time(dev_id, timer):

    """
    :param dev_id: device id
    :param timer: such as 1, 2, 3
    :return: Object alarm time if it is exist in database otherwise return None.
    """
    try:
        alert_list = AlarmTime.objects.filter(dev__id=dev_id, timer=timer)
        if alert_list is None:
            return None
        for row in alert_list:
            return row

    except Exception as ex:
        logger.debug(ex)
        return None


# Check expired AlarmTime. This mean, action must perform
def check_expired_alarm_time(dev_id, timer, now_time):
    """
    :param dev_id:
    :param timer:
    :param now_time:
    :return: If alarm time is expired will be return true, otherwise return false
    """
    alarm_time = get_specified_alarm_time(dev_id, timer)
    if alarm_time is None:
        logger.debug("Alert null")
        return False

    if alarm_time.active is True and now_time >= alarm_time.time:
        return True

    return False


# Check expired  Alarm Time. This mean, action must perform
def check_expired_alarm_time_object(alarm_time, now_time):

    if alarm_time.active is True and now_time >= alarm_time.time:
        return True

    return False


# Save object and try catch when perform
def save(obj):
    try:
        obj.save()
    except Exception as ex:
        logger.debug(ex)
        return False

    return True


# Save record monitor room temp
def save_temp_record(now_time, value, type):
    """
    :param now_time:
    :param value: float
    :param type: record for minute such as '1m', '5m', '30m',
    record for hour such as '1h'
    record for day such as '1d'
    record for month such as '1mo'
    record for year such as '1y'
    :return: if save success return True, otherwise return False
    """
    try:
        value = float("{0:.2f}".format(value))
        temp = Temperature(time=now_time, value=value, type=type)
        temp.save()

        return True
    except Exception as ex:
        logger.debug(ex)
        return False


# Get all record save room temp
def get_temp_record_list():
    try:
        temp_list = Temperature.objects.all()
        return temp_list
    except Exception as ex:
        logger.debug(ex)
        return None


# Get all record between two time point
def get_temp_record_between_two_point_time(start_time, end_time, type):
    try:
        temp_list = Temperature.objects.filter(type=type).filter(time__lte=end_time).filter().filter(time__gte=start_time).\
            order_by('id')

        return temp_list
    except Exception as ex:
        logger.debug(ex)
        return None


# Get avg value between two time point
def get_temp_average_between_two_time(start_time, end_time, type):

    try:
        value = Temperature.objects.filter(type=type).filter(time__lte=end_time).filter().filter(time__gte=start_time).\
            aggregate(Avg('value'))
        return value['value__avg']
    except Exception as ex:
        logger.debug(ex)
        return None


def create_alarm_by_temp(dev, action, condition, value):
    """
    :param dev: device object
    :param action: on or off
    :param condition:
    :param value:
    :return:
    """

    try:
        alarm_temp = AlarmTemp(dev=dev, action=action, condition=condition, value=value, active=True)
        alarm_temp.save()
        # print 'return object is not None'
        return alarm_temp
    except Exception as ex:
        logger.debug(ex)
        return None


def get_alarm_by_temp_list():
    try:
        return AlarmTemp.objects.all()
    except Exception as ex:
        logger.debug(ex)
        return None


# Get alarm by temp following dev_id
def get_alarm_by_temp(dev_id):
    try:
        alarm_by_temp_list = AlarmTemp.objects.filter(dev__id=dev_id)
        if alarm_by_temp_list is None:
            return None

        for row in alarm_by_temp_list:
            return row

        return None

    except Exception as ex:
        logger.debug(ex)
        return None


# Get enable alert by temp for device
def get_enabled_alarm_by_temp_for_device(dev_id):
    try:
        alert_by_temp = AlarmTemp.objects.filter(dev__id=dev_id, active=True)
        for row in alert_by_temp:
            return row
        return None
    except Exception as ex:
        logger.debug(ex)
        return None


# Get enable alert by temp
def get_enabled_alarm_by_temp_list():
    try:
        alert_by_temp_list = AlarmTemp.objects.filter(active=True)
        return alert_by_temp_list

    except Exception as ex:
        print ex
        logger.debug(ex)
        return None


# Enable a alarm by temp if it is exist
def enable_alarm_by_temp(dev_id, condition, action, value):
    alarm_by_temp = get_alarm_by_temp(dev_id)
    if alarm_by_temp is None:
        return False

    try:
        alarm_by_temp.condition = condition
        alarm_by_temp.action = action
        alarm_by_temp.active = True
        alarm_by_temp.value = value
        alarm_by_temp.true_count = 0
        alarm_by_temp.false_count = 0
        alarm_by_temp.save()

        return True
    except Exception as ex:
        logger.debug(ex)
        return False


# Disable alarm by temp
def disable_alarm_by_temp(dev_id):
    alarm_by_temp = get_alarm_by_temp(dev_id)
    if alarm_by_temp is None:
        return False

    try:
        alarm_by_temp.condition = None
        alarm_by_temp.active = False
        alarm_by_temp.action = None
        alarm_by_temp.value = None
        alarm_by_temp.true_count = 0
        alarm_by_temp.false_count = 0
        alarm_by_temp.save()

        return True
    except Exception as ex:
        logger.debug(ex)
        return False


def reset_count_alarm_by_temp(dev_id):
    alarm_by_temp = get_alarm_by_temp(dev_id)
    if alarm_by_temp is None:
        return False

    try:
        alarm_by_temp.false_count = 0
        alarm_by_temp.true_count = 0

        alarm_by_temp.save()
        return True
    except Exception as ex:
        logger.debug(ex)
        return False


def reset_true_count_alarm_by_temp_object(alarm_by_temp):

    """
    Reset true_count for true condition
    :param alarm_by_temp: object
    :return:
    """
    try:

        if alarm_by_temp.true_count == 0:
            return False

        alarm_by_temp.true_count = 0

        alarm_by_temp.save()
        return True
    except Exception as ex:
        logger.debug(ex)
        return False


def reset_false_count_alarm_by_temp_object(alarm_by_temp):

    """
    Reset false_count for false condition
    :param alarm_by_temp: object
    :return:
    """
    try:

        if alarm_by_temp.false_count == 0:
            return False

        alarm_by_temp.false_count = 0

        alarm_by_temp.save()
        return True
    except Exception as ex:
        logger.debug(ex)
        return False




def reset_count_alarm_by_temp_object(alarm_by_temp):
    """
    :param alarm_by_temp: alarm by temp object
    :return:
    """
    try:
        alarm_by_temp.false_count = 0
        alarm_by_temp.true_count = 0

        alarm_by_temp.save()
        return True
    except Exception as ex:
        logger.debug(ex)
        return False


def change_value_true_count_alarm_by_temp(alarm_by_temp, action):
    """
    :param alarm_by_temp: alarm_by temp object
    :param action: if 1 increase true_count value, otherwise decrease true_count value
    :return: true is success, false is not success
    """
    try:
        if action == 1:
            alarm_by_temp.true_count = (alarm_by_temp.true_count + 1)
        else:
            if alarm_by_temp.true_count == 0:
                return False

            alarm_by_temp.true_count = (alarm_by_temp.true_count - 1)

        alarm_by_temp.save()
        return True
    except Exception as ex:
        logger.debug(ex)
        return False


def change_value_false_count_alarm_by_temp(alarm_by_temp, action):
    """
    :param alarm_by_temp: alarm_by temp object
    :param action: if 1 increase false_count value, otherwise decrease false_count value
    :return: true is success, false is not success
    """
    try:
        if action == 1:
            alarm_by_temp.false_count = (alarm_by_temp.false_count + 1)
        else:
            if alarm_by_temp.false_count == 0:
                return False

            alarm_by_temp.false_count = (alarm_by_temp.false_count - 1)

        alarm_by_temp.save()
        return True
    except Exception as ex:
        logger.debug(ex)
        return False


def is_true_condition(alarm_by_temp):
    """
    :param alarm_by_temp: Alarm using temperature object
    :return: If alarm have a true_count is equal amount. Return true, return false
    """
    if alarm_by_temp.true_count >= settings.MAX_COUNT:
        return True

    return False


def is_false_condition(alarm_by_temp):
    """
    :param alarm_by_temp: Alarm using temperature object
    :return: if alarm have a false_count is equal amount, return True, return false
    """

    if alarm_by_temp.false_count >= settings.MAX_COUNT:
        return True

    return False


def is_true_alarm_by_temp(alarm_by_temp, temp_value):
    """
    :param alarm_by_temp: Alarm using temperature object
    :param temp_value: Now temperature
    :return: True if true condition otherwise return False
    """
    ret = False

    temp_value = float(temp_value)


    if alarm_by_temp.condition == 'gt':
        ret = temp_value > alarm_by_temp.value
    elif alarm_by_temp.condition == 'gte':
        ret = temp_value >= alarm_by_temp.value
    elif alarm_by_temp.condition == 'eq':
        ret = temp_value == alarm_by_temp.value
    elif alarm_by_temp.condition == 'lt':
        ret = temp_value < alarm_by_temp.value
    elif alarm_by_temp.condition == 'lte':
        ret = temp_value <= alarm_by_temp.value

    # print 'temp_value: %s, condition: %s, alarm_by_temp: %s, result: %s' % (temp_value, alarm_by_temp.condition,
    # alarm_by_temp.value, ret)

    return ret


# Check condition is true or false
def get_true_alarm_by_temp_list(temp_value):
    result_list = []
    alert_list = AlarmTemp.objects.filter(active=True)
    if alert_list is None or len(alert_list) == 0:
        return None

    ret = False

    for alert in alert_list:

        if alert.condition == 'gt':
            ret = temp_value > alert.value
        elif alert.condition == 'gte':
            ret = temp_value >= alert.value
        elif alert.condition == 'eq':
            ret = temp_value == alert.value
        elif alert.condition == 'lt':
            ret = temp_value < alert.value
        elif alert.condition == 'lte':
            ret = temp_value <= alert.value

        # If condition is true. add device to result list
        if ret:

            result_list.append(alert)

    if len(result_list) == 0:
        return None

    return result_list


def perform_alarm_by_temp(alarm):
    """
    :param alarm: alarm by temperature object
    :return:Not return value
    """

    ret = is_true_condition(alarm)
    if ret:
        action = alarm.action
        if action == 'on':
            action = 0
        elif action == 'off':
            action = 1

        if action is None or (action != 0 and action != 1):
            logger.debug('Have error when control device. Can not get device status')
            return

        status = controldev.get_device_status_to_code(alarm.dev.id)
	logger.debug('now_status %s' % status)
	logger.debug('action: %s, code %s' % (action, alarm.action))
        if int(status) == action:
            reset_count_alarm_by_temp_object(alarm)
            logger.debug('Action can not perform again')
            return

        status = controldev.control_device(alarm.dev.id, action)
        status = controldev.change_status_to_code(status)

        # Have error
        if int(status) != action:
            logger.debug('Have error when control device. Unknown device status')
            reset_count_alarm_by_temp_object(alarm)
            return
        else:
            logger.debug('Control device success')
            reset_count_alarm_by_temp_object(alarm)
            return

    ret = is_false_condition(alarm)
    if ret:
        action = alarm.action
        if action == 'on':
            action = 0
        elif action == 'off':
            action = 1


        if action is None or (action != 0 and action != 1):
            logger.debug('Have error. Unknown action')
            return

        status = controldev.get_device_status_to_code(alarm.dev.id)

        if int(status) == action:
            logger.debug('Action can not perform again')
            reset_count_alarm_by_temp_object(alarm)
            return

        status = controldev.control_device(alarm.dev.id, action)
        status = controldev.change_status_to_code(status)

        # Have error
        if int(status) != action:
            logger.debug('Have error when control device')
            print reset_count_alarm_by_temp_object(alarm)
            return
        else:
            logger.debug('Control device success')
            reset_count_alarm_by_temp_object(alarm)
            return


def check_alarm_by_temp(temp_value):

    """
    Check alarm by temperature
    :return: do not return
    """

    enabled_alarm_by_temp_list = get_enabled_alarm_by_temp_list()
    if enabled_alarm_by_temp_list is None:
        return

    # print len(enabled_alarm_by_temp_list)

    for alarm in enabled_alarm_by_temp_list:

        ret = is_true_alarm_by_temp(alarm, temp_value)
        if ret:
            change_value_true_count_alarm_by_temp(alarm, 1)
            reset_false_count_alarm_by_temp_object(alarm)
        else:
            change_value_false_count_alarm_by_temp(alarm, 1)
            reset_true_count_alarm_by_temp_object(alarm)

        perform_alarm_by_temp(alarm)


def get_option_list_with_specified_type(type):
    """
    :param type: type of option such as bitrate, size, fps
    :return:list of option
    """
    try:
        option_list = VideoOption.objects.filter(type=type).order_by('id')
        return option_list
    except Exception as ex:
        logger.debug(ex)
        return None


# Get default value of type
def get_default_value_specified_type(type):
    """
    :param type: type of option such as bitrate, size, fps
    :return:list of option
    """
    logger.debug(type)
    try:
        option_list = VideoOption.objects.filter(type=type).filter(default=type)
        if option_list.exists():
            return option_list[0]
        else:
            return None
    except Exception as ex:
        logger.debug(ex)
        return None





