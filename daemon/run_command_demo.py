import subprocess
file_name = '/var/www/video/out.h264'
command = '/usr/bin/raspivid -t 0 -w 960 -h 540 -fps 25 -b 500000 -vf -o %s' % file_name
print command
subprocess.call(command)
print 'finish'

