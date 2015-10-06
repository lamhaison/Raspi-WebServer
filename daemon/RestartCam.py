#!/usr/bin/python
import commands
import time
import os
import sys


from datetime import datetime, timedelta
from django.utils import timezone

sys.path.append("/var/www/web-app/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videostreaming.settings")
from viewcam.api import controldev, apitimer, videoapi
import logging
logger = logging.getLogger(__name__)
from threading import Thread

# Thread run video
def threaded_function(cmd):
    commands.getoutput(cmd)

if __name__ == '__main__':
    try:
        ret = controldev.check_exist_raspivid_process()
        if ret:
            # Video a mode streaming
            is_streaming = controldev.get_status_camera()
            if is_streaming == 'on':
                logger.debug('Start video in streaming mode')
                result = controldev.control_camera('start')
                logger.debug(result)

            else:
                logger.debug('Start video in write to file mode')
                controldev.control_camera('stop')
                cmd = controldev.get_command_run_raspivid_process_without_streaming()
                result = commands.getoutput(cmd)
                logger.debug(result)
        else:
            logger.debug('Start video in write to file mode')
            controldev.control_camera('stop')
            cmd = controldev.get_command_run_raspivid_process_without_streaming()
            result = commands.getoutput(cmd)
            logger.debug(result)
    except Exception as ex:
        logger.debug(ex)


