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
import logging
logger = logging.getLogger(__name__)
from threading import Thread

# Thread run video
def threaded_function(cmd):
    commands.getoutput(cmd)

if __name__ == '__main__':
    try:
        videoapi.run_using_crontab()
    except Exception as ex:
        logger.debug(ex)


