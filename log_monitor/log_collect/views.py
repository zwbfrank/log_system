from django.shortcuts import render
from user_manage.models import Config,Log
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
            lsys = LogCollect(str(log_type))
            lsys.insert_syslog()
        except Exception as e:
            raise e
        return  render(request,'log_collect/collect_index.html')



def system(request):
    logs = Log.objects.all().order_by('-create_at')[:100]
    context = {'logs': logs}
    if request.method == 'POST':
        lsys = LogCollect('system')
        lsys.insert_syslog()
        logs = Log.objects.all().order_by('-create_at')[:100]
        context = {'logs': logs}
    return render(request,'log_collect/system_display.html',context)
