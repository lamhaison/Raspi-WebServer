#!/usr/bin/python
import commands
import time
import os
import sys
from threading import Thread





# Check alertTime, if alertTime > nowTime then action will be perform
def checkExpired(alertTime):
    nowTime = datetime.now()
    return alertTime > nowTime


sys.path.append("/var/www/web-app/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videostreaming.settings")
flag = 1
import django
django.setup()

from viewcam.api import controldev
from viewcam.api import accessdb
from viewcam.api import apitimer
from datetime import datetime, timedelta
from django.utils import timezone
from viewcam.models import Device, Temperature, AlarmTemp, AlarmTime
import logging
from django.conf import settings
logger = logging.getLogger(__name__)

data = []
nowtime = apitimer.get_now_time_without_second()
next_time = nowtime + timedelta(minutes=1)


def checkAlarmTime():
    timerList = accessdb.get_enabled_alarm_time_list()
    if timerList is None:
        return
    if len(timerList) == 0:
        return

    for timer in timerList:
        nowTime = apitimer.get_now_time_without_second()
        ret = accessdb.check_expired_alarm_time_object(timer, nowTime)
        if ret:
            msg =  'disable dev %s timer %s' % (timer.id, timer.timer)
            logger.debug(msg)
            ret = accessdb.disable_alarm_time(timer.dev.id, timer.timer)
            action = ''
            if timer.action == 'on':
                action = 0
            else:
                action = 1

            controldev.control_device(timer.dev.id, action)
            if ret is False:
                log = 'can not disable timer %s %s' % (timer.id, timer.timer)
                logger.debug(log)


def getTempAverage(temp_value, now_time):
    global next_time
    global data

    logger.debug(temp_value)
    logger.debug(now_time)
    if now_time < next_time:
        data.append(temp_value)
    else:
        sum = 0
        logger.debug(now_time)

        for record in data:
            sum = (sum + record)

        # Don't have data to calculate average value
        if len(data) == 0:
            return

        average = float(sum / len(data))
        msg = 'temp_average = %s' % average
        logger.debug(msg)
        ret = accessdb.save_temp_record(now_time - timedelta(minutes=1), average, '1m')
        msg = 'result insert record to db: %s' % ret
        logger.debug(msg)
        accessdb.check_alarm_by_temp(temp_value)

        if (now_time.minute % 5) == 0:
            avg_value = accessdb.get_temp_average_between_two_time(now_time - timedelta(minutes=5),
                                                                   now_time - timedelta(minutes=1), '1m')

            accessdb.save_temp_record(now_time, avg_value, '5m')

        if (now_time.minute % 10) == 0:
            avg_value = accessdb.get_temp_average_between_two_time(now_time - timedelta(minutes=5),
                                                                   now_time, '5m')
            accessdb.save_temp_record(now_time, avg_value, '10m')

        if (now_time.minute % 30) == 0:
            # time is X.30
            interval = 10

            # time is X.00
            if now_time.minute == 0:
                interval = 20
            avg_value = accessdb.get_temp_average_between_two_time(now_time - timedelta(minutes=interval),
                                                                   now_time, '10m')
            accessdb.save_temp_record(now_time, avg_value, '30m')

        if now_time.minute == 0:
            avg_value = accessdb.get_temp_average_between_two_time(now_time - timedelta(minutes=30),
                                                                   now_time, '30m')
            accessdb.save_temp_record(now_time, avg_value, '1h')

        if now_time.hour == 0 and now_time.minute == 0:
            avg_value = accessdb.get_temp_average_between_two_time(now_time - timedelta(days=23), now_time, '1h')
            accessdb.save_temp_record(now_time, avg_value, '1d')



        # Reset list temp for next_time
        data = []
        next_time = next_time + timedelta(minutes=1)
        data.append(temp_value)


# Thread run video
def threaded_function(cmd):
    commands.getoutput(cmd)

# Update status of device when raspi was booted
dev_list = accessdb.get_device_list()
for dev in dev_list:
    status = controldev.get_device_status(dev.id)

    # Update status of device
    controldev.update_status_device(dev.id, status)

    # Reset alarm by tem when raspi was booted.
    accessdb.reset_count_alarm_by_temp_object(dev)

isOn = False
thread = None
while True:


    # Check cam to write to file
    ret = controldev.check_exist_raspivid_process()
    if ret is False:
        command = controldev.get_command_run_raspivid_process_without_streaming()
        thread = Thread(target=threaded_function, args=(command,))
        thread.start()

    now_time = apitimer.get_full_unit_now_time()
    logger.debug(now_time)
    # Check time
    if now_time.second == 0 or now_time.second == 1:
        print now_time
        checkAlarmTime()

    temp_value = controldev.get_temp()
     # High temp
    if temp_value >= settings.FIRE_TEMPERATURE:
        logger.debug('Start alert fire')
        msg = 'TEMP %s' % temp_value
        logger.debug(msg)
        result = controldev.control_alert_fire(1)
        isOn = True
    else:
        logger.debug('Stop alert fire')
        if isOn:
            isOn = False
            result = controldev.control_alert_fire(0)

    getTempAverage(temp_value, now_time)

    time.sleep(0.9)
