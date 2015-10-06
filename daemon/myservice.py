#!/usr/bin/python
import commands
import time
import os
import sys

from datetime import datetime
from django.utils import timezone



#Check alertTime, if alertTime > nowTime then action will be perform
def checkExpired(alertTime):
	nowTime = datetime.now()
	return alertTime > nowTime
sys.path.append("/var/www/web-app/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videostreaming.settings")
flag = 1
from viewcam.api import controldev
from viewcam.api import accessdb
from viewcam.api import apitimer
from viewcam.models import Device, Temperature, AlertTemp, AlertTime
import logging
logger = logging.getLogger(__name__)


def checkAlertTimer():
	timerList = accessdb.getEnableAlertTimeList()
	if timerList is None:
		print 'retur'
		return
	if len(timerList) == 0:
		return

        for timer in timerList:
        	nowTime = apitimer.getNowTime()
        	ret = accessdb.checkExpiredTimerObject(timer, nowTime)
		if ret:
			print 'disable dev %s timer %s' % (timer.id, timer.timer)
			ret = accessdb.disableAlertTime(timer.dev.id, timer.timer)
			action = ''
			if timer.action == 'on':
				action = 1
			else:
				action = 0
			
			controldev.controlDeviceLed(timer.dev.id, action)
			if ret is False:
			
				log = 'can not disable timer %s %s' % (timer.id, timer.timer)
				logger.debug(log)
				

#i = 0
while (True):

	checkAlertTimer()
	time.sleep(1)




	'''
	command = 'echo "%s" >> /root/Desktop/test.log' % dev.dev_name
	commands.getoutput('date >> /root/Desktop/test.log')
	commands.getoutput('/bin/bash /usr/local/rrd/getStatis.sh >> /root/Desktop/test.log')
	i = i + 1
	if i > 30:
		commands.getoutput('/bin/bash /usr/local/rrd/makegraph.sh >> /root/Desktop/test.log')
		i = 0
	time.sleep(1)
	'''

