from django.shortcuts import render,redirect
from user_manage.models import Config,Log,InfoLog,ErrorLog
from django.http import HttpResponseRedirect,HttpResponse

import os
import sys
import configparser

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from log_collect_script import *


# Create your views here.
def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get("is_login")
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/user_manage/login')
    return inner

@auth
def collect_index(request):
    return render(request,'log_collect/collect_index.html')

@auth
def config(request):
    message = ''
    context = {}
    if request.method == 'GET':
        return render(request,'log_collect/config.html')
    elif request.method == 'POST':
        try:
            cfg = MyConfigParser()
            log_type = request.POST.get('logtype')
            path = request.POST.get('path')
            level = request.POST.get('level')
            if log_type=='' or path=='' or level=='':
                message = 'please fill out the form'
                return render(request,'log_collect/config.html',{'msg':message})               
            if not cfg.has_section(log_type):
                cfg[str(log_type)] = {
                    'path' : path,
                    'log_type': log_type,
                    'level': level,
                }
                cfg.auto_write()
            else:
                lc = LogCollect(str(log_type))
                if level == 'sys':
                    lc.insert_syslog()
                elif level == 'info':
                    lc.insert_info()
                elif level == 'error':
                    lc.insert_error()
        except Exception as e:
            raise e
            # message = 'please fill out the form'
            # return render(request,'log_collect/config.html',{'msg':message})
        return  render(request,'log_collect/collect_index.html')

@auth
def system(request):
    message = ''
    logs = Log.objects.order_by('-create_at')[:100]
    context = {'logs': logs}
    if request.method == 'POST':
        # section = request.POST.get('section')
        lc = LogCollect('system')
        lc.insert_syslog()
        message = 'please wait a moment,is flushing'
        logs = Log.objects.order_by('-create_at')[:100]
        context = {'logs': logs,'msg':message}
        return render(request,'log_collect/system_display.html',context)

    return render(request,'log_collect/system_display.html',context)

@auth
def info(request):
    cfg = MyConfigParser()
    logs = InfoLog.objects.order_by('-create_at')[:100]
    message = ''
    context = {'logs': logs}
    if request.method == 'POST':
        section = request.POST.get('logtype')
        if not section or section not in cfg.sections():
            message = 'please fill out this field.'
            return render(request,'log_collect/info_display.html',{'msg':message})
        else:
            lc = LogCollect(section)
            lc.insert_info()
            logs = InfoLog.objects.order_by('-create_at')[:100]
            context = {'logs': logs}
    return render(request,'log_collect/info_display.html',context)

@auth
def error(request):
    cfg = MyConfigParser()
    logs = ErrorLog.objects.order_by('-create_at')[:100]
    context = {'logs': logs}
    if request.method == 'POST':
        section = request.POST.get('logtype')
        if not section or section not in cfg.sections():
            message = 'please fill out this field.'
            return render(request,'log_collect/error_display.html',{'msg':message})
        lc = LogCollect(section)
        lc.insert_error()
        logs = ErrorLog.objects.order_by('-create_at')[:100]
        context = {'logs': logs}
    return render(request,'log_collect/error_display.html',context)