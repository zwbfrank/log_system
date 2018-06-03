from django.shortcuts import render

from datetime import datetime

from .models import Log

# Create your views here.
def index(request):
    time = datetime.now()
    context = {'time':time}
    return render(request,'user_manage/index.html',context)

def base(request):
    return render(request,'user_manage/base.html')

def register(request):
    return render(request,'user_manage/register.html')

def login(request):
    return render(request,'user_manage/login.html')