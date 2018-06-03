import os,sys,django



# sys.path.append(os.path.abspath(os.path.join(BASE_DIR,os.pardir)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "log_monitor.settings") 

django.setup()

import re
import time
from time import sleep
from datetime import datetime
# import pymysql


import configparser

from user_manage.models import Log

import logging
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler
from random import Random

    # hdlr = logging.handlers.RotatingFileHandler(LOG_FILE,maxBytes=1024*1024,backupCount=40)或
    # hdlr = logging.handlers.TimedRotatingFileHandler(LOG_FILE,when='M',interval=1,backupCount=40)
# logger = logging.getLogger('mylogger')
# logger.setLevel(logging.)

# def log_info():
#     logger = logging.getLogger('mylogger')
#     logger.setLevel(logging.INFO)
#     th = TimedRotatingFileHandler('test.log',when='S',interval=10,backupCount=10)
#     formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
#     th.setFormatter(formatter)
#     logger.addHandler(th)
#     while True:
#         logger.info('test message')
#         sleep(1)


# def persude_error_code(path,spcnum):
#     while True:
#         count = 1
#         if os.path.exists(path):
#             logging.basicConfig(path)
#             logger = logging.getLogger()
#             while True:
#                 if os.path.getsize(path)>=spcnum:
#                     break
#                 msg='test message '+str(count)+'.'
#                 logger.error(msg)
#                 count = count+1
#                 random_sec = random_time(100)
#                 sleep(random_sec)
#             os.move(path,direct)
#             path = os.mknod(filename)
#         sleep(5)


# def info(path):
#     pass



# def logging_out(log_path):


#     logging.basicConfig(level=logging.ERROR,
#                         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                         datefmt='%b %d %Y %H:%M:%S',
#                         filename=log_path,
#                     )
#     logger = logging.getLogger()
#     logger

    
#     while True:
        
#     msg = ''
#     logger.error(msg)



pattern_error = re.compile(r'error.log$')
pattern_info =  re.compile(r'info.log$')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MyConfigParser(configparser.ConfigParser):
    
    def __init__(self,config_file='log_system_config.ini'):
        self.config_file = os.path.join(BASE_DIR,config_file)
        super(MyConfigParser,self).__init__()
        self.read(self.config_file)

    def get_sections(self):
        return self.sections()

    def get_options(self,section):
        return self.options(section)

    def get_conf_dict(self,section):
        conf_dict = {}
        for option in self.get_options(section):
            value = self.get(section,option)
            conf_dict[option] = int(value) if value.isdigit() else value
        return conf_dict

    def add_option(self,section,option,value=None):
        self[section][option] = value
        return option

    def auto_write(self):
        with open(self.config_file,'w') as config_file:
            self.write(config_file)



# class Config():

#     def __init__(self, config_file="log_system_config.ini"):
#         file_path = os.path.join(BASE_DIR,config_file)
#         self.cfg = configparser.ConfigParser()
#         self.cfg.read(file_path)

#     def get_sections(self): 
#         return self.cfg.sections()

#     def hasSection(self,section):
#         sections = get_sections()
#         if section in sections:
#             return True
#         return False

#     def get_options(self, section):
#         return self.cfg.options(section)

#     def get_content(self, section):
#         result = {}
#         for option in self.get_options(section):
#             value = self.cfg.get(section, option)
#             result[option] = int(value) if value.isdigit() else value
#         return result

#     def add_sections(self,section):
#         self.cfg[section] = {}
#         return self.cfg[section]

#     def add_options(self,section,option,value):
#         option = self.add_sections(section)
#         option[str(option)] = value


    
class BaseLog(object):
    def __init__(self,log_type='system',path='/var/log/syslog',level='sys',file_name=None,file_size=None):
        self.log_type = log_type
        self.path = path
        self.level = level
        self.file_name = file_name
        self.file_size = file_size


class LogCollect(BaseLog):
    """docstring for LogCollect"""
    def __init__(self, section):
        self.cfg = MyConfigParser()
        self.config = self.cfg.get_conf_dict(section)
        super(LogCollect, self).__init__(**self.config)

    def get_offset_dict(self):
        offset_dict = self.cfg.get_conf_dict('Offset')
        return offset_dict
        
    def get_info_file(self):
        file_list = os.listdir(self.path)
        if file_list:
            for file in file_list:
                if re.match(pattern_info,file):
                    return file

    def get_error_file(self):
        file_list = os.listdir(self.path)
        if file_list:
            for file in file_list:
                if re.match(pattern_error,file):
                    return file

    def get_sys_file(self):
        return os.path.basename(self.path)
        
    def read_sys_file(self):
        file = self.path
        self.file_name = os.path.basename(file)
        with open(file) as f:
            lines = self.save_sys_offset(f)
        return lines

    def read_info_file(self):
        self.file_name = self.get_info_file()
        if file:
            with open(os.path.join(self.path,file)) as f:
                lines = self.save_offset(f)
        return lines

    def insert_syslog(self):
        lines = self.read_sys_file()
        for line in lines:
            log = Log()
            log.log_type = self.log_type
            log.level = self.level
            log.content = line
            log.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log.save()

    def insert(self):
        lines = self.read_info_file()
        for line in lines:
            log = Log()
            log.log_type = self.log_type
            log.level = self.level
            log.content = line
            log.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log.save()

    def reset_offset(self):
        self.cfg.remove_option('Offset',str(self.file_name))

    def is_newfile(self,offset):
        # offset_dict = self.cfg.get_conf_dict('Offset')
        if os.path.isfile(self.path):
            self.file_name = os.path.basename(self.path)
            # offset = offset_dict[str(self.file_name)]
            if int(offset) > os.path.getsize(self.path):
                return True
            else:
                # print(str(offset)+' '+str(os.path.getsize(self.path)))
                return False
        # file_path = os.path.join(self.path,self.file_name)
        # file_size = os.path.getsize(file_path)
        # if int(offset) > os.path.getsize(file_size):
        #     return True
        # return False

    def is_new_syslog(self,offset):
        if os.path.isfile(self.path):
            self.filename = os.path.basename(self.path)
            if int(offset) > os.path.getsize(self.path):
                return True
        return False

    def save_sys_offset(self,f_obj):
        self.cfg = MyConfigParser()
        # if is_newfile():
        #     self.reset_offset()
        if self.cfg.has_section('Offset'):
            if self.cfg.has_option('Offset',str(self.file_name)):
                offset = self.cfg.get('Offset',str(self.file_name))
                if self.is_new_syslog(offset):
                    lines = f_obj.readlines()
                    offset = f_obj.tell()
                    self.cfg['Offset'][str(self.file_name)] = str(offset)
                    self.cfg.auto_write()
                f_obj.seek(int(offset))
                lines = f_obj.readlines()
                offset = f_obj.tell()
                self.cfg['Offset'][str(self.file_name)] = str(offset)
                self.cfg.auto_write()
            else:
                lines = f_obj.readlines()
                offset = f_obj.tell()
                self.cfg.add_option('Offset',str(self.file_name),str(offset))
                self.cfg.auto_write()
        else:
            lines = f_obj.readlines()
            offset = f_obj.tell()
            self.cfg.add_section('Offset')
            self.cfg.add_option('Offset',str(self.file_name),str(offset))
            self.cfg.auto_write() 
        return lines

    def save_offset(self,f_obj):
        # cfg = MyConfigParser()
        # if is_newfile():
        #     self.reset_offset()
        if self.cfg.has_section('Offset'):
            if self.cfg.has_option('Offset',str(self.file_name)):
                offset = self.cfg.get('Offset',str(self.file_name))
                # if is_newfile(offset):
                #     self.reset_offset()
                #     lines = f_obj.readlines()
                #     offset = f_obj.tell()
                #     self.cfg['Offset'][str(self.file_name)] = str(offset)
                #     self.cfg.auto_write()
                f_obj.seek(int(offset))
                lines = f_obj.readlines()
                offset = f_obj.tell()
                self.cfg['Offset'][str(self.file_name)] = str(offset)
                self.cfg.auto_write()
            else:
                lines = f_obj.readlines()
                offset = f_obj.tell()
                self.cfg.add_option('Offset',str(self.file_name),str(offset))
                self.cfg.auto_write()
        else:
            lines = f_obj.readlines()
            offset = f_obj.tell()
            self.cfg.add_section('Offset')
            self.cfg.add_option('Offset',str(self.file_name),str(offset))
            self.cfg.auto_write() 
        return lines

def main():
    lsys = LogCollect('system')
    lt2 = LogCollect('')
    print(lc.is_newfile(1200000))
    # lc.insert_syslog()
    

if __name__ == '__main__':
    # main()
    print(BASE_DIR)




    # print(os.path.abspath(os.path.join(BASE_DIR, 'user_manage/models.py')))
    # print(BASE_DIR)
    # print(os.path.join(BASE_DIR,'/user_manage/models.py'))
    # print(os.path.abspath(__file__))
    # print(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))


    # log = Log()
    # log.log_type = 'test1'
    # log.level = 'test1'
    # log.content = 'test1'
    # log.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # log.save()


    # conn,cursor= db_connect()
    # level = 'error'
    # log_type = 'system'
    # content = 'This is a test.'
    # create_at = datetime.now()
    # insert = 'INSERT INTO log (level,log_type,content,create_at) VALUES (%s,%s,%s,%s)'
    # cursor.execute(insert,(level,log_type,content,create_at))
    # conn.commit()
    # db_close(conn,cursor)

