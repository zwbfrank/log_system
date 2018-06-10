"""log_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from user_manage import views
# from django.contrib.auth import urls as auth_urls
# from log_collect import views

# from django.contrib.auth import urls as auth_urls
 
 

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^user_manage/', include('user_manage.urls',namespace='user_manage')),
    url(r'^log_collect/', include('log_collect.urls',namespace='log_collect')),
    url(r'^admin/', admin.site.urls),

]
