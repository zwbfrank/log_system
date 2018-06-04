from django.shortcuts import render
from user_manage.models import Config,Log,InfoLog,ErrorLog
from django.http import HttpResponseRedirect,HttpResponse

import os
import sys
import configparser

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from log_collect_script import *


# Create your views here.
def collect_index(request):
    return render(request,'log_collect/collect_index.html')

def config(request):
    if request.method == 'GET':
        return render(request,'log_collect/config.html')
    elif request.method == 'POST':
        try:
            cfg = MyConfigParser()
            log_type = request.POST.get('logtype')
            path = request.POST.get('path')
            level = request.POST.get('level')
            if not cfg.has_section(log_type):
                cfg[str(log_type)] = {
                    'path' : path,
                    'log_type': log_type,
                    'level': level,
                }
                cfg.auto_write()
            lc = LogCollect(str(log_type))
            if level == 'sys':
                lc.insert_syslog()
            elif level == 'info':
                lc.insert_info()
            elif level == 'error':
                lc.insert_error()
        except Exception as e:
            raise e
        return  render(request,'log_collect/collect_index.html')

def system(request):
    logs = Log.objects.all().order_by('-create_at')[:100]
    context = {'logs': logs}
    if request.method == 'POST':
        # section = request.POST.get('section')
        lc = LogCollect('system')
        lc.insert_syslog()
        logs = Log.objects.all().order_by('-create_at')[:100]
        context = {'logs': logs}
    return render(request,'log_collect/system_display.html',context)

def info(request):
    cfg = MyConfigParser()
    logs = InfoLog.objects.all().order_by('-create_at')[:100]
    context = {'logs': logs}
    if request.method == 'POST':
        section = request.POST.get('logtype')
        if not section or section not in cfg.sections():
            return HttpResponse('<html>please fill correct log type</html')
        lc = LogCollect(section)
        lc.insert_info()
        logs = InfoLog.objects.all().order_by('-create_at')[:100]
        context = {'logs': logs}
    return render(request,'log_collect/info_display.html',context)

def error(request):
    cfg = MyConfigParser()
    logs = ErrorLog.objects.all().order_by('-create_at')[:100]
    context = {'logs': logs}
    if request.method == 'POST':
        section = request.POST.get('logtype')
        if not section or section not in cfg.sections():
            return HttpResponse('<html>please fill correct log type</html')
        lc = LogCollect(section)
        lc.insert_error()
        logs = ErrorLog.objects.all().order_by('-create_at')[:100]
        context = {'logs': logs}
    return render(request,'log_collect/error_display.html',context)



