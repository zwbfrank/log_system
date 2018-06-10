

from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm


from datetime import datetime

# Create your views here.

def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get("is_login")
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('user_manage/login')
    return inner


def index(request):
    time = datetime.now()
    context = {'time':time}
    return render(request,'user_manage/index.html',context)


def base(request):
    return render(request,'user_manage/base.html')

def register(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email    = form.cleaned_data['email']

            user = UserInfo.objects.create(username=username,password=password,email=email)
            request.session['username'] = username
            return redirect(request,'user_manage/login',context)
    else:
        form =UserForm()
        context = {'form': form}
        return render(request,'user_manage/register.html',context)

def login(request):
    message = ''

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserInfo.objects.filter(username=username, password=password).count()
        if user:
            request.session['is_login'] = True
            request.session['username'] = username
            return redirect('/')
        else:
            message = "username or password error"

    return render(request, 'user_manage/login.html', {'msg': message})

def logout(request):
    try:
        request.session['is_login'] = False
        del request.session['username']
    except KeyError:
        pass
    return HttpResponse('OK')