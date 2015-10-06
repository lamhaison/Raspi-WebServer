#!/usr/bin/python
import commands
import time
import os
import sys

from datetime import datetime, timedelta
from django.utils import timezone


sys.path.append("/var/www/web-app/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videostreaming.settings")
flag = 1
from viewcam.api import controldev
from viewcam.api import accessdb
from viewcam.api import apitimer
from viewcam.models import Device, Temperature, AlarmTemp, AlarmTime
import logging
from time import sleep
logger = logging.getLogger(__name__)

while (True):
    accessdb.check_alarm_by_temp()
    time.sleep(3)
