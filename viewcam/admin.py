__author__ = 'root'
from django.contrib import admin
from viewcam.models import Device, Temperature, AlarmTemp, AlarmTime, DeviceHistory, VideoOption
from django.contrib import messages

admin.autodiscover()


class DeviceView(admin.ModelAdmin):
    # Update if have been device to add or to delete, sync data on db
    def insert_all_alarm_record(self, request, queryset):
        try:
            for obj in queryset:
                obj.initial_all_alarm_record()
        except Exception as ex:
            msg = "Can't initial alarm record in database. Please check again"
            self.message_user(request, msg, level=messages.ERROR)
            return
        self.message_user(request, "Successfully initial alarm record in database.")


    insert_all_alarm_record.short_description = 'Initial alarm record in db'
    actions = [insert_all_alarm_record]
    list_display = ('dev_name', 'desc', 'status')
    list_editable = ['dev_name', 'desc']


class AlarmTempView(admin.ModelAdmin):
    list_display = ('dev', 'action', 'condition', 'value', 'true_count', 'false_count', 'active')


class AlarmTimeView(admin.ModelAdmin):
    list_display = ('dev', 'timer', 'action', 'time', 'active')


class TempView(admin.ModelAdmin):
    list_display = ('time', 'value', 'type')


class VideoOptionView(admin.ModelAdmin):
    list_display = ('desc', 'type', 'value', 'default')
    list_filter = ['type', 'value', 'default']
    list_editable = ['desc', 'type', 'value']
    readonly_fields = ['default']

    def set_default_value(self, request, queryset):

        # Check select only one option to set to be default value
        if len(queryset) >= 2:
            msg = 'Can not select two option. Please chose only one option'
            self.message_user(request, msg, level=messages.ERROR)
            return

        try:
            for obj in queryset:
                obj.set_is_default_value()
        except Exception as ex:
            msg = 'Can not set this option to be default value'
            self.message_user(request, msg, level=messages.ERROR)
            return

        self.message_user(request, "Successful set this option to be default value.")

    set_default_value.short_description = 'Set to be default value'
    actions = [set_default_value]




class HistoryDeviceStatusView(admin.ModelAdmin):
    list_display = ('dev', 'time', 'from_status', 'to_status')
    list_filter = ['dev', 'from_status', 'to_status']
    list_per_page = 20

# class TempView(admin.ModelAdmin):


admin.site.register(Device, DeviceView)
admin.site.register(AlarmTemp, AlarmTempView)
admin.site.register(AlarmTime, AlarmTimeView)
admin.site.register(Temperature, TempView)
admin.site.register(DeviceHistory, HistoryDeviceStatusView)
admin.site.register(VideoOption, VideoOptionView)