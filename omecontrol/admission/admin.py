from django.contrib import admin
from . import models


@admin.register(models.Grant)
class GrantAdmin(admin.ModelAdmin):
  list_display = ('name', 'protocol', 'application', 'direction')