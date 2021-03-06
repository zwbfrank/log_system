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
from django.conf.urls import url
# from django.contrib import admin
from log_collect import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$',views.collect_index,name='collect_index'),
    url(r'^config/',views.config,name='config'),
    url(r'^system_display/',views.system,name='system'),
    url(r'^info_display/',views.info,name='info'),
    url(r'^error_display/',views.error,name='error'),

]
