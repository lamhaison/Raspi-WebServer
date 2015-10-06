#!/usr/bin/python
import commands
import time
import os
import sys


from datetime import datetime, timedelta
from django.utils import timezone


sys.path.append("/var/www/web-app/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videostreaming.settings")
from viewcam.api import videoapi
from viewcam.api import apitimer
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        now_date = apitimer.get_now_time_without_second()
        interval_delete = settings.INTERVAL_DAY_DELETE
        pre_date = now_date - timedelta(minutes=interval_delete)
        logger.debug(interval_delete)
        # print interval_delete
        pre_date = apitimer.get_time_with_format_from_time('%Y-%m-%d', pre_date)
        # print pre_date
        path = settings.VIDEO_DIR

        command = 'rm -rf %s/%s*' % (path, pre_date)
        result = commands.getoutput(command)
        logger.debug(result)
        logger.debug(command)
        # print command
        # logger.debug(pre_date)
    except Exception as ex:
        logger.debug(ex)


