from django.test import TestCase
from viewcam.models import Device, Temperature, AlarmTemp, AlarmTime
from viewcam.api import accessdb, apitimer, controldev, dbapi, videoapi
from datetime import datetime, timedelta
from time import sleep
from viewmodel import device
import json

import logging
logger = logging.getLogger(__name__)


class HistoryDeviceStatusCase(TestCase):
    def test_check_change_status_device(self):
        # Create device
        dev = accessdb.create_device('dev1', 'dev1')
        self.assertEqual(dev is None, False)


        # Check status device. Default of device status is OFF
        status = controldev.get_device_status(dev.id)
        self.assertEqual(status, 'OFF')



        # Update status device
        ret = accessdb.update_status_device_input_obj(dev, status)
        # Because status default is OFF, update new status is OFF. Return False
        self.assertEqual(ret, False)



        # Change status
        status = 'ON'
        ret = accessdb.update_status_device_input_obj(dev, status)
        self.assertEqual(ret, True)


        # Get list alarm by time for device which just insert to db
        alarm_list = accessdb.get_alarm_time_list_from_device_pk(dev.id)
        for row in alarm_list:
            log = '%s %s' % (row.dev.dev_name, row.timer)
            logger.debug(log)
        self.assertEqual(alarm_list is None, False)
        self.assertEqual(len(alarm_list), 0)

        # Get list alarm by temp for device
        alarm_by_temp = accessdb.get_alarm_by_temp(dev.id)
        self.assertEqual(alarm_by_temp is None, False)
        self.assertEqual(alarm_by_temp.dev.dev_name, dev.dev_name)

        # Get device status
        dev_test = accessdb.get_device_from_pk(dev.id)
        self.assertEqual(dev_test is None, False)
        self.assertEqual(dev_test.status, 'ON')

        # Create History
        now_time = apitimer.get_now_time_with_second()
        from_status = 'OFF'
        to_status = 'ON'
        ret = accessdb.insert_history_device_status(dev, from_status, to_status)
        self.assertEqual(ret, True)

        # Get list device
        history_list = accessdb.get_list_history_device_status(dev.id)
        self.assertEqual(len(history_list), 1)


class VideoApiCase(TestCase):
    def test_generate_name_file(self):
        name_file = videoapi.get_name_video('mp4')
        self.assertEqual(name_file is None, False)

    def test_get_list_file(self):
        result_list = videoapi.get_list_video()

        now_time = apitimer.get_now_time_without_second()
        logger.debug(now_time)
        for row in result_list:
            ret = videoapi.check_true_time(now_time, 1, row)
            logger.debug(ret)

class ConnectionCase(TestCase):
    def test_connect_db(self):
        cur = dbapi.create_connection_to_database()
        self.assertEqual(cur is None, False)

    def test_get_all_device(self):
        result = dbapi.get_all_device()
        self.assertEqual(result is None, False)
        print result


        detail_device_list = []
        for row in result:
            dev = Device(row[0], row[1], row[2])
            detail_device_list.append(dev)

        logger.debug(detail_device_list)

        for dv in detail_device_list:
            detail_dev = '%s %s %s' % (dv.id, dv.dev_name, dv.desc)
            logger.debug(detail_dev)



        self.assertEqual(len(detail_device_list), 4)




class AlertTempCase(TestCase):

    def testCreateAlertCondtion(self):
        dev_id = 1
        dev = accessdb.get_device_from_pk(1)
        dev_name = 'dev%s' % dev_id
        if dev is None:
            dev = accessdb.create_device(dev_name, '')
        self.assertEqual(dev.dev_name, dev_name)


        #Create AlertCondition
        alertCon = accessdb.create_alarm_by_temp(dev, 'on', 'gt', 37.5)
        ret = alertCon is None
        self.assertEqual(ret, False)

        #Get condition
        alertCon = accessdb.get_alarm_by_temp(dev_id)
        ret = alertCon is None
        self.assertEqual(ret, False)

        #Disable condtion alert
        ret = accessdb.disable_alarm_by_temp(dev_id)
        self.assertEqual(ret, True)

        #check disable alertContion
        alertCon = accessdb.get_alarm_by_temp(dev_id)
        ret = alertCon is None
        self.assertEqual(ret, False)
        self.assertEqual(alertCon.active, False)

        #Enable condtion
        condition = 'gte'
        action = 'on'
        value = 40

        ret = accessdb.enable_alarm_by_temp(dev_id, condition, action, value)
        self.assertEqual(ret, True)
        alertCon = accessdb.get_alarm_by_temp(dev_id)
        ret = alertCon is None
        self.assertEqual(ret, False)
        self.assertEqual(alertCon.active, True)
        self.assertEqual(alertCon.action, action)
        self.assertEqual(alertCon.value, value)
        self.assertEqual(alertCon.condition, condition)



        dev2 = accessdb.create_device('dev2', '')
        self.assertEqual(dev2.dev_name, 'dev2')
        alertCon = accessdb.create_alarm_by_temp(dev2, action, condition, value)

        alertList = accessdb.get_alarm_by_temp_list()
        self.assertEqual(len(alertList), 2)

        ret = alertCon is None
        self.assertEqual(ret, False)
        self.assertEqual(alertCon.condition, condition)

        alertList = accessdb.get_true_alarm_by_temp_list(50)
        self.assertEqual(len(alertList), 2)

        #self.assertEqual(ret, True)

        alarm_object = accessdb.get_enabled_alarm_by_temp_for_device(1)
        self.assertEqual(alarm_object.active, True)
        ret = accessdb.is_true_alarm_by_temp(alarm_object, 50)
        self.assertEqual(ret, True)
        ret = accessdb.is_true_alarm_by_temp(alarm_object, 20)
        self.assertEqual(ret, False)

        ret = accessdb.disable_alarm_by_temp(alarm_object.dev.id)
        self.assertEqual(ret, True)
        alarm_object = accessdb.get_enabled_alarm_by_temp_for_device(1)
        self.assertEqual(alarm_object is None, True)
        ret = accessdb.enable_alarm_by_temp(1, action, condition, value)
        self.assertEqual(ret, True)
        alarm_object = accessdb.get_enabled_alarm_by_temp_for_device(1)
        self.assertEqual(alarm_object is None, False)

        old_value = alarm_object.true_count
        ret = accessdb.change_value_true_count_alarm_by_temp(alarm_object, 0)
        self.assertEqual(ret, False)
        alarm_object = accessdb.get_alarm_by_temp(1)
        self.assertEqual(alarm_object is None, False)
        self.assertEqual(alarm_object.true_count, 0)

        old_value = alarm_object.true_count
        ret = accessdb.change_value_true_count_alarm_by_temp(alarm_object, 1)
        self.assertEqual(ret, True)
        self.assertEqual(alarm_object.true_count, old_value + 1)

        ret = accessdb.reset_count_alarm_by_temp_object(alarm_object)
        self.assertEqual(ret, True)

        self.assertEqual(alarm_object.true_count, 0)
        self.assertEqual(alarm_object.false_count, 0)



        old_value = alarm_object.false_count
        ret = accessdb.change_value_false_count_alarm_by_temp(alarm_object, 0)
        self.assertEqual(ret, False)

        old_value - alarm_object.false_count
        ret = accessdb.change_value_false_count_alarm_by_temp(alarm_object, 1)
        self.assertEqual(ret, True)
        self.assertEqual(alarm_object.false_count, old_value + 1)

        ret = accessdb.is_true_alarm_by_temp(alarm_object, 20)
        self.assertEqual(ret, False)

        ret = accessdb.is_true_condition(alarm_object)
        self.assertEqual(ret, False)

        accessdb.change_value_true_count_alarm_by_temp(alarm_object, 1)
        ret = accessdb.reset_true_count_alarm_by_temp_object(alarm_object)
        self.assertEqual(ret, True)
        self.assertEqual(alarm_object.true_count, 0)

        accessdb.change_value_false_count_alarm_by_temp(alarm_object, 1)
        ret = accessdb.reset_false_count_alarm_by_temp_object(alarm_object)
        self.assertEqual(ret, True)
        self.assertEqual(alarm_object.false_count, 0)


        accessdb.check_alarm_by_temp()


class DeviceTestCase(TestCase):
    def testCreateDevice(self):

        #Create device 1
        dev = accessdb.create_device('dev1', '')
        self.assertEqual(dev.dev_name, 'dev1')

        #Create duplicate device 1
        dev = accessdb.create_device('dev1', '')
        self.assertEqual(dev, None)



        # Creat device 2
        dev = accessdb.create_device('dev2', '')
        self.assertEqual(dev.dev_name, 'dev2')


        # Get device following name
        dev = accessdb.get_device_from_name('dev2')
        self.assertEqual(dev.dev_name, 'dev2')

        # Get device flowwing device id
        # CHECK ERROR_TEST

        dev = accessdb.get_device_from_pk(1)
        self.assertEqual(dev.dev_name, 'dev1')


        #Get list device
        dev_list = accessdb.get_device_list()
        self.assertEqual(len(dev_list), 2)


#Test AlertTime
class AlertTimeCase(TestCase):
    def testCreateAlertTime(self):

        #Create device from dev name
        dev = accessdb.create_device('dev1', '')
        self.assertEqual(dev.dev_name, 'dev1')

        alert = accessdb.create_alarm_using_time(dev, 'on', datetime.now(), 1)
        self.assertEqual(alert.dev.dev_name, dev.dev_name)


        self.assertEqual(len(accessdb.get_alarm_time_list()), 1)

        alertList = accessdb.get_alarm_time_list_from_device_pk(dev.id)

        self.assertEqual(len(alertList), 1)

        alertList = accessdb.get_alarm_time_list_from_device_name(dev.dev_name)
        self.assertEqual(len(alertList), 1)
        #Access queryset and compare dev_name
        for row in alertList:
            self.assertEqual(row.dev.dev_name, dev.dev_name)

        #Get specfied timer
        alert = accessdb.get_specified_alarm_time(dev.id, 1)
        self.assertEqual(alert.dev.id, dev.id)
        self.assertEqual(alert.timer, 1)

        #Disable timer
        accessdb.disable_alarm_time(dev.id, 1)

        alert = accessdb.get_specified_alarm_time(dev.id, 1)
        self.assertEqual(alert.active, False)

        #Get device is not exist
        alert = accessdb.get_specified_alarm_time(dev.id, 2)
        ret = alert is None
        self.assertEqual(ret, True)

        action = 'off'
        nowTime = apitimer.get_now_time_without_second()
        accessdb.enable_alarm_time(dev.id, action, nowTime, 1)
        alert = accessdb.get_specified_alarm_time(dev.id, 1)
        self.assertEqual(alert.active, True)
        self.assertEqual(alert.time, nowTime)
        self.assertEqual(alert.action, action)


        timerList = accessdb.get_enabled_alarm_time_list()
        self.assertEqual(len(timerList), 1)

        for timer in timerList:
            testTime = timer.time
            nowTime = apitimer.get_now_time_without_second()
            nowTime = nowTime - timedelta(hours=1)
            ret = accessdb.check_expired_alarm_time_object(timer, nowTime)
            self.assertEqual(ret, False)

            nowTime = nowTime + timedelta(hours=1)
            ret = nowTime is None
            self.assertEqual(ret, False)
            ret = accessdb.check_expired_alarm_time_object(timer, nowTime)
            self.assertEqual(ret, True)




        #Check expired time
        sleep(1)
        time = datetime.now()
        isExpired = accessdb.check_expired_alarm_time(dev.id, 1, time)
        self.assertEqual(isExpired, True)



        #Get interval between two time point
        lastTime = time + timedelta(hours=10, days=2, minutes=10)
        intervalTime = lastTime - time
        self.assertEqual(intervalTime.days, 2)
        self.assertEqual(intervalTime.seconds, (60 * 60 * 10 + 10 * 60))


        #Create new device 2
        dev = accessdb.create_device('dev2', '')
        self.assertEqual(dev.dev_name, 'dev2')
        alert = accessdb.create_alarm_using_time(dev, 'on', nowTime, 1)
        self.assertEqual(alert.dev, dev)

#Test Timer. calulator between two time point
class TimerTest(TestCase):
    def testCalculateTimer(self):
        nowTime = datetime.now()
        alertTime = nowTime + timedelta(hours=3, days=2)
        stringTime = apitimer.get_interval(nowTime, alertTime)
        self.assertEqual(stringTime, "2Day3H")

        #nowTime = apitimer.getAlertTime(2015, 1, 30, 10, 20)
        ret = nowTime is None
        self.assertEqual(ret, False)

        alertTime = nowTime + timedelta(hours=0, days=2)
        stringTime = apitimer.get_interval(nowTime, alertTime)
        self.assertEqual(stringTime, "2Day")


        alertTime = nowTime + timedelta(hours=0, days=0, seconds=60)
        stringTime = apitimer.get_interval(nowTime, alertTime)
        self.assertEqual(stringTime, "1M")

        alertTime = nowTime + timedelta(hours=12, days=2, seconds=60)
        stringTime = apitimer.get_interval(nowTime, alertTime)
        self.assertEqual(stringTime, "2Day12H1M")


        alertTime = nowTime + timedelta(hours=0, days=0, seconds=30)
        stringTime = apitimer.get_interval(nowTime, alertTime)
        self.assertEqual(stringTime, "1M")


        alertTime = nowTime + timedelta(days=10, hours=0, seconds=0)
        stringTime = apitimer.get_interval(nowTime, alertTime)
        self.assertEqual(stringTime, "10Day")


        alertTime = nowTime + timedelta(days=0, hours=5, seconds=0)
        stringTime = apitimer.get_interval(nowTime, alertTime)
        self.assertEqual(stringTime, "5H")


        alertTime = nowTime + timedelta(days=0, hours=5, minutes=10)
        stringTime = apitimer.get_interval(nowTime, alertTime)
        self.assertEqual(stringTime, "5H10M")


        alertTime = nowTime - timedelta(days=0, hours=5, minutes=10)
        stringTime = apitimer.get_interval(nowTime, alertTime)
        self.assertEqual(stringTime, None)

        alertTime = apitimer.get_alarm_time(2015, 2, 10, 23, 49)
        ret = alertTime is None
        self.assertEqual(ret, False)
        testTime = apitimer.get_now_time_without_second()
        ret = testTime is None
        self.assertEqual(ret, False)
        #print testTime
        #print apitimer.getInterValBetweenTime(testTime, alertTime)


    def testListInforTimerEnable(self):

        dev = accessdb.get_device_from_pk(1)
        if dev is None:
            dev = accessdb.create_device('dev1', 1)

        alerTimer = accessdb.get_specified_alarm_time(1, 1)
        if alerTimer is None:
            alerTimer = accessdb.create_alarm_using_time(dev, 'on', apitimer.get_now_time_without_second() + timedelta(hours=1), 1)
            alerTimer = accessdb.create_alarm_using_time(dev, 'on', apitimer.get_now_time_without_second() + timedelta(hours=1), 2)

        timerList = accessdb.get_enabled_alarm_time_list()
        self.assertEqual(len(timerList), 2)
        if timerList is None:
            return


        devList = accessdb.get_device_list()
        if devList is None:
            return

        inforList = {}
        for dev in devList:


            timerList = accessdb.get_alarm_time_list_from_device_pk(dev.id)

            if timerList is None:
                return
            detailTimerList = {}
            for timer in timerList:
                nowTime = apitimer.get_now_time_without_second()
                remainTime = apitimer.get_interval(nowTime, timer.time)
                action = timer.action
                if remainTime is None:
                    remainTime = ''
                    action = ''

                detail = {}
                detail['action'] = action
                detail['remain'] = remainTime

                key = 'timer%s' % timer.timer
                detailTimerList[key] = detail

            key = 'dev%s' % dev.id
            inforList[key] = detailTimerList

        jsonObj = json.dumps(inforList)

        print jsonObj[1]
        print inforList


# Save temp record
class TemperatureCase(TestCase):
    def testSaveTempRecord(self):
        temp_list = accessdb.get_temp_record_list()
        self.assertEqual(len(temp_list), 0)

        #insert value 1
        value = 10
        nowTime = apitimer.get_now_time_without_second()
        ret = accessdb.save_temp_record(nowTime, value, '1m')
        self.assertEqual(ret, True)

        #insert value 2
        value = 20
        ret = accessdb.save_temp_record(nowTime, value, '1m')
        self.assertEqual(ret, True)
        listTemp = accessdb.get_temp_record_list()
        self.assertEqual(len(listTemp), 2)

        #Get between time that have no element
        nowTime = nowTime + timedelta(hours=1)
        endTime = nowTime + timedelta(hours=20)
        list = accessdb.get_temp_record_between_two_point_time(nowTime, endTime, '1m')
        self.assertEqual(len(list), 0)


        #Avg list have two element
        nowTime = nowTime - timedelta(hours=1)
        endTime = nowTime + timedelta(hours=20)
        list = accessdb.get_temp_record_between_two_point_time(nowTime, endTime, '1m')
        self.assertEqual(len(list), 2)

        avg = accessdb.get_temp_average_between_two_time(nowTime, endTime, '1m')
        self.assertEqual(avg, 15.0)


        #Avg empty list
        nowTime = nowTime + timedelta(hours=1)
        endTime = nowTime + timedelta(hours=20)
        list = accessdb.get_temp_record_between_two_point_time(nowTime, endTime, '1m')
        self.assertEqual(len(list), 0)

        avg = accessdb.get_temp_average_between_two_time(nowTime, endTime, '1m')
        self.assertEqual(avg, None)


        accessdb.save_temp_record(nowTime, 11.2, '5m')
        accessdb.save_temp_record(nowTime, 11.5, '5m')
        accessdb.save_temp_record(nowTime, 11.2, '1m')
        list = accessdb.get_temp_record_between_two_point_time(nowTime, endTime, '5m')
        self.assertEqual(len(list), 2)
        avg_temp = accessdb.get_temp_average_between_two_time(nowTime, endTime, '5m')
        self.assertEqual(avg_temp, 11.35)

        list = accessdb.get_temp_record_between_two_point_time(nowTime, endTime, '1m')
        self.assertEqual(len(list), 1)

    def testGetTemperature(self):

        data = []
        time = apitimer.get_now_time_without_second()
        next_time = time + timedelta(minutes=1)





