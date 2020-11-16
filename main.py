import os
from service import Service, find_syslog
import time
import logging
from logging.handlers import SysLogHandler


class Jarvis(Service):
    def __init__(self, *args, **kwargs):
        super(Jarvis, self).__init__(*args, **kwargs)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.INFO)

    def run(self):
        while not self.got_sigterm():
            self.logger.info("I'm working...")
            time.sleep(5)

    def stop(self, block=False):
        print('shutting down, sir.')
        return super().stop(block=block)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        sys.exit('Syntax: {} COMMAND'.format(sys.argv[0]))
    cmd = sys.argv[1].lower()
    service = Jarvis('jarvis', pid_dir = '/tmp')

    if cmd == 'start':
        service.start()
    elif cmd == 'stop':
        service.stop()
    elif cmd == 'status':
        if service.is_running():
            print("I'm running, sir.")
        else:
            print("I'm not currently running, sir")
    else:
        sys.exit("I'm not sure what to do with your instruction: {}".format(cmd))
    
