from django.contrib import admin

from .models import UserInfo
from .models import Log
from .models import Config
from .models import InfoLog
from .models import ErrorLog

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Log)
admin.site.register(Config)
admin.site.register(InfoLog)
admin.site.register(ErrorLog)