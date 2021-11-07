from django.contrib import admin
from . import models


@admin.register(models.PushConfig)
class PushConfigAdmin(admin.ModelAdmin):
  list_display = ('name','vhost', 'app', 'stream', 'active' )