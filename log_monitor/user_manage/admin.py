from django.contrib import admin

from .models import UserInfo
from .models import Log
from .models import Config

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Log)
admin.site.register(Config)