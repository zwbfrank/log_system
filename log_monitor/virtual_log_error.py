#!/usr/bin/env python
import os

# BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# sys.path.append(os.path.abspath(os.path.join(BASE_DIR,os.pardir)))

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "log_monitor.settings") 

# django.setup()
import time
from time import sleep
# from datetime import datetime
# import random
import logging
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler


def log_error():
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.ERROR)
    th = TimedRotatingFileHandler('/opt/test_project/test_log_type_1/test_1_error.log',
                                    when='S',interval=10,backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    th.setFormatter(formatter)
    logger.addHandler(th)
    while True:
        logger.error('test error message.')
        sleep(1)


def main():
    log_error()


if __name__ == '__main__':
    main()
    