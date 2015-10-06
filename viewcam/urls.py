from django.conf.urls import patterns, url
from viewcam import views, ajaxurl

urlpatterns = patterns('',

	# html url
	url(r'^$', views.template, name='index'),
	url(r'test$', views.test, name='test'),
	url(r'highchart$', views.load_high_chart, name='test'),
	url(r'testcal$', views.openCal, name='testcal'),
	url(r'template$', views.template, name='template'),



	# ajax url
	url(r'^gettime$', ajaxurl.get_time, name='getTime'),
	url(r'^getrealinfo$', ajaxurl.get_info, name='getinfo'),
	url(r'^gettemp$', ajaxurl.get_temp, name='getTem'),
	url(r'^control/dev(?P<device_id>\d+)/(?P<action_id>\d+)/$', ajaxurl.control_device, name='control'),
	url(r'getallstatus', ajaxurl.get_all_status, name='get_all_status'),
	url(r'getstatus/dev(?P<device_id>\d+)/$', ajaxurl.get_device_status, name='get_status'),


	# set alarm time
	url(r'^alarm/dev(?P<device_id>\d+)/timer(?P<timer>\d+)/(?P<action>\w+)/(?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{4})/(?P<hour>\d{1,2})/(?P<minute>\d{1,2})/$',
		ajaxurl.alarm_by_date, name='alarm_date'),

	url(r'^alarm/dev(?P<device_id>\d+)/timer(?P<timer>\d+)/(?P<action>\w+)/(?P<minute>\d{1,10})/$',
		ajaxurl.alarm_by_minute, name='alarm_minute'),

	url(r'^alarmtemp/dev(?P<device_id>\d+)/(?P<action>\w+)/(?P<condition>\w+)/(?P<value>\d{1,10})/$',
		ajaxurl.alarm_by_temp, name='alarm_by_temp'),

	url(r'^alarmtemp/dev(?P<device_id>\d+)/remove/$',
		ajaxurl.remove_alarm_by_temp, name='remove_alarm_by_temp'),

	url(r'^alarm/dev(?P<device_id>\d+)/timer(?P<timer>\d+)/remove/$',
		ajaxurl.remove_alarm_by_time, name='remove_alarm_by_time'),


	#get alert time infor
	url(r'^alarmtime/dev(?P<device_id>\d+)/timer(?P<timer>\d+)/$', ajaxurl.get_alarm_by_time, name='get_alarm_by_time'),
	url(r'^alarmtime/all/$', ajaxurl.get_all_alarm_by_time, name='get_all_alarm_by_time'),

	url(r'^alarmtemp/dev(?P<device_id>\d+)/$', ajaxurl.get_alarm_by_temp, name='get_alarm_by_temp'),
	url(r'^alarmtemp/all$', ajaxurl.get_all_alarm_by_temp, name='get_alarm_by_temp'),

	url(r'^gettemplist/(?P<interval>\d{1,10})/(?P<unit>\w+)$', ajaxurl.get_temp_list, name='get_temp_list'),


    # control camera

    url(r'^controlcam/(?P<action>\w+)$', ajaxurl.control_camera, name='control_cam'),

    # px, bit_rate, frame_ps, sharpness, contrast, brightness, saturation, iso, ev, ex, awb
    url(r'^controlcam/(?P<px>\w+)/(?P<bit_rate>\w+)/(?P<frame_ps>\w+)/(?P<sharpness>-?\w+)/(?P<contrast>-?\w+)'
        r'/(?P<brightness>\w+)/(?P<saturation>-?\w+)/(?P<iso>\w+)/(?P<ev>-?\w+)/(?P<ex>\w+)/(?P<awb>\w+)$',
        ajaxurl.set_property_camera, name='set_property_cam'),



	url(r'^testhightchart/$', ajaxurl.test_high_chart, name='test_hight_chart'),



	#action/(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/(?P<hour>\d{2})/(?P<minute>\d{2})/$





)

