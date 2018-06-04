from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email    = models.EmailField(max_length=125)
    
    def __str__(self):
        return self.username

    class Meta:
    	db_table = 'user'


class Log(models.Model):
    level = models.CharField(max_length=50)
    log_type = models.CharField(max_length=50)
    content = models.TextField(max_length=225)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
    	db_table = 'log'


class InfoLog(models.Model):
    log_type = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    content = models.TextField(max_length=225)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'info'


class ErrorLog(models.Model):
    log_type = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    content = models.TextField(max_length=225)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'error'


class Config(models.Model):
    path = models.CharField(max_length=225)
    log_type = models.CharField(max_length=50)
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.log_type

    class Meta:
        db_table = 'config'
