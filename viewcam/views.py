from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import Http404
from django_ajax.decorators import ajax
from django.utils import timezone
import json
import datetime
import os
from django.contrib.auth.decorators import login_required
from viewcam.api import accessdb, apitimer, dbapi
from viewmodel import timerview, changeview, alarmtemp
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

@login_required(login_url='./admin/login')
def index(request):
    return render(request, 'viewcam/index.html', None)


def test(request):
    return render(request, 'viewcam/ajaxtest.html', None)


def load_high_chart(request):
    return render(request, 'viewcam/highchart_demo.html', None)

def openCal(request):
    return render(request, 'viewcam/datedemo.html')


@login_required(login_url='/accounts/login/')
def template(request):
    logger.debug(apitimer.get_real_time())
    device_list = accessdb.get_device_list()
    # device_list = dbapi.get_all_device()

    timer_list = settings.TIMER_LIST

    # Detail timer
    detail_alarm_by_time_list = []

    # Get detail info off all timer
    for dev in device_list:
        result_list = accessdb.get_alarm_time_list_from_device_pk(dev.id)
        for row in result_list:
            timer = timerview.Timer()
            timer.dev_id = dev.id
            timer.timer = row.timer
            now_time = apitimer.get_now_time_without_second()
            remain_time = apitimer.get_interval(now_time, row.time)

            # If timer is expire
            if remain_time is None or remain_time == '':
                timer.action = ''
                timer.remain = ''
            else:
                timer.action = changeview.change_action_view(row.action)
                timer.remain = remain_time
            detail_alarm_by_time_list.append(timer)




    # if device_list is None or len(device_list) == 0:
    #    device_list = settings.DEV_LIST

    alarm_temp_list = accessdb.get_alarm_by_temp_list()
    detail_alarm_temp_list = []
    for row in alarm_temp_list:
        detail = alarmtemp.AlarmTemp()
        if row.active is False:
            detail.action = ''
            detail.dev_id = row.dev.id
            detail.condition = ''
            detail.temp_value = ''

        else:
            detail.action = changeview.change_action_view(row.action)
            detail.dev_id = row.dev.id
            detail.condition = row.condition
            detail.temp_value = row.value
        detail_alarm_temp_list.append(detail)


    logger.debug(apitimer.get_real_time())

    size_option_list = accessdb.get_option_list_with_specified_type('size')
    kbitrate_option_list = accessdb.get_option_list_with_specified_type('bitrate')
    frame_psecond_option_list = accessdb.get_option_list_with_specified_type('fps')

    return render(request, 'viewcam/template.html', {'devList': device_list, 'timerList': timer_list,
        'detailList': detail_alarm_by_time_list, 'alarmTempList': detail_alarm_temp_list,
                        'test_value': 10,
                        'size_option_list': size_option_list,
                        'kbitrate_option_list': kbitrate_option_list,
                        'frame_psecond_option_list': frame_psecond_option_list})



'''


@ajax
def getTime(request):
    #print timezone.localtime(timezone.now())
    newTime = datetime.datetime.now().strftime("%H:%M:%S")
    #print newTime
    return HttpResponse(json.dumps({"time": newTime}),
            content_type="application/json")

@ajax
def getTem(request):
    #print timezone.localtime(timezone.now())
    newTime = datetime.datetime.now().strftime("%S")
    #print newTime
    return HttpResponse(json.dumps({"tem": newTime}),
            content_type="application/json")

@ajax
def controlDevice(request, device_id, action_id):
    print "Control device"
    print device_id
    print action_id
    status = ControlDevice.controlDeviceLed(device_id, action_id)
    #return render(request, 'viewcam/index.html', None)
    return HttpResponse(json.dumps({'dev': device_id, 'status': status}),
            content_type='application/json')

@ajax
def getStatusAll(request):
    print 'Get all device'
    print ControlDevice.getStatusAllDevice()

    return HttpResponse(json.dumps({'dev1': 'On', 'dev2': 'Off'}),
            content_type='application/json')

@ajax
def getStatusDevice(request, device_id):
    print 'get status device'
    print device_id
    #Get device
    status = 'On'
    print ControlDevice.getStatusDevice(device_id)
    return HttpResponse(json.dumps({'dev': device_id, 'status': status}), content_type='application/json')

'''



# Create your views here.
