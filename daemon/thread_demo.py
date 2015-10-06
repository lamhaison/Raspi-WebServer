from threading import Thread
from time import sleep
import commands
def threaded_function(arg, name):
    command = '/usr/bin/raspivid -t 0 -w 960 -h 540 -fps 25 -b 500000 -vf -o /var/www/video/out.h264'
    commands.getoutput(command)

if __name__ == "__main__":
    thread = Thread(target = threaded_function, args = (1000, 'thread1'))
    thread.start()
    print 'end command'
    while True:
	print 'run demo'
	ret = thread.is_alive()
	print ret
	
	
    # thread.join()
    # print "thread finished...exiting"
