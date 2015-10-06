from django.db import models

# Create your models here.
import logging
logger = logging.getLogger(__name__)
from django.conf import settings



class Device(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="Pin")
    dev_name = models.CharField(max_length=10, unique=True)
    desc = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=5, default='OFF')

    class Meta:
        # verbose_name = 'device'
        db_table = 'devices'

    # Insert alarm by temp and alarm by time record
    def initial_all_alarm_record(self):
        timer_list = settings.TIMER_LIST
        try:
            list_alarm_by_time = AlarmTime.objects.filter(dev__id=self.id)
            # Check the first insert alarm by time
            if list_alarm_by_time is None or len(list_alarm_by_time) == 0:
                for timer in timer_list:
                    alarm_by_time = AlarmTime(dev=self, action=None, time=None, timer=timer, active=False)
                    alarm_by_time.save()

            list_alarm_by_temp = AlarmTemp.objects.filter(dev__id=self.id)
            # Check the first insert alarm by temp
            if list_alarm_by_temp is None or len(list_alarm_by_temp) == 0:
                alarm_by_temp = AlarmTemp(dev=self, action=None, condition=None, value=None, active=False)
                alarm_by_temp.save()
        except Exception as ex:
            logger.debug(ex)

    def __unicode__(self):
            return self.dev_name


class AlarmTime(models.Model):
    dev = models.ForeignKey('Device')
    action = models.CharField(max_length=3, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    timer = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        msg = '%s timer %s' % (self.dev, self.timer)
        return msg

    class Meta:
        # verbose_name = 'alert'
        db_table = 'alarmtime'




class AlarmTemp(models.Model):
    dev = models.ForeignKey('Device')
    action = models.CharField(max_length=3, blank=True, null=True)
    condition = models.CharField(max_length=8, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    active = models.BooleanField(default=False)
    true_count = models.IntegerField(default=0)
    false_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.dev.dev_name

    class Meta:
        # verbose_name = 'alert'
        db_table = 'alarmtemp'


class Temperature(models.Model):
    time = models.DateTimeField()
    value = models.FloatField()
    type = models.CharField(max_length=10, default='1m')

    def __unicode__(self):
        msg = '%s value %s' % (self.time, self.value)
        return msg

    class Meta:
        db_table = 'temp'


class DeviceHistory(models.Model):
    dev = models.ForeignKey('Device')
    time = models.DateTimeField()
    from_status = models.CharField(max_length=5, default='ON')
    to_status = models.CharField(max_length=5, default='OFF')


    def __unicode__(self):
        msg = '%s from %s to %s' % (self.dev.dev_name, self.from_status, self.to_status)
        return msg

    class Meta:
        # verbose_name = 'alert'
        db_table = 'history'


class VideoOption(models.Model):

    option_type_list = settings.VIDEO_TYPE_OPTION
    desc = models.CharField(max_length=50, verbose_name='Description')
    type = models.CharField(max_length=50, verbose_name='Parameter Types', choices=option_type_list)
    value = models.CharField(max_length=50, verbose_name='Value')
    default = models.BooleanField(default=False, verbose_name='Set default Value')

    # Set option to default value
    def set_is_default_value(self):
        try:
            list_object = VideoOption.objects.filter(type=self.type).filter(default=True)
            if list_object is None:
                logger.error('list video option have same type is None')
                return

            # Remove default value.
            for row in list_object:
                row.default = False
                row.save()

            self.default = True
            self.save()
        except Exception as ex:
            logger.error(ex)
            raise RuntimeError("Can't set this option to be default value")




    class Meta:
        db_table = 'video_option'
