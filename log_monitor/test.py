import configparser
import os

# class config(configparser.ConfigParser):
#     """docstring for config"""
#     def __init__(self, arg):
#         super(config, self).__init__()

# def db_close(conn,cursor):
#     cursor.close()
#     conn.close()

# def pymysql_conn():
#     # databases config
#     config = {
#         'db': 'ppss_log',
#         'user': 'log_user',
#         'password': 'hsplan.2017',
#         'host': 'rm-bp1mnhth64d8zx0q6.mysql.rds.aliyuncs.com',
#         'port': 3306,
#         'charset': 'utf8',
#     }
#     try:
#         conn = pymysql.connect(**config)
#     except:
#         print("Cannot connect into database.")
    
#     # cursor = conn.cursor()
#     return conn

# def db_connect():
#     config = {
#         'db': 'log_system',
#         'user': 'root',
#         'password': '84218421',
#         'host': 'localhost',
#         'port': 3306,
#         'charset': 'utf8',
#         # 'HOST': 'localhost',
#         # 'PORT': 3306,
#         # 'NAME': 'log_system',
#         # 'USER': 'root',
#         # 'PASSWORD': '84218421',
#         # 'CHARSET': 'utf8',
#     }
#     try:
#         conn = pymysql.connect(**config)
#         cursor = conn.cursor()
#     except Exception as e:
#         print("Can't connect into database see %s"%e)
#     return conn,cursor

# def search_new_file(dirname):
#     dir_list_file = os.listdir(dirname)
#     # print(dir_list_file)
#     if dir_list_file is not None:
#         new_file_list = [file for file in dir_list_file if pattern_new_log.match(file)]
#     return new_file_list

# def get_info_file(dirname):
#     new_file_list = search_new_file(dirname)
#     for file in new_file_list:
#         if pattern_info_file.match(file):
#             return file

# def get_error_file(dirname):
#     new_file_list = search_new_file(dirname)
#     for file in new_file_list:
#         if pattern_error_file.match(file):
#             return file

def main():
    

    cfg = configparser.ConfigParser()
    cfg.read('log_system_config.ini')
    items = cfg.items()
    print(cfg['defaultLog'])
    for item in items:


    # cfg['defaultLog']['content'] ='This is a test'
    # with open('log_system_config.ini','w') as conf:
    #     cfg.write(conf)

if __name__ == '__main__':
    main()