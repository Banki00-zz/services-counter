from django.contrib import admin
from .models import *


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'price', 'sum_for_worker', 'date_add')


class TypeOfWorkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'fix_percent', 'user')


admin.site.register(TypeOfWork, TypeOfWorkAdmin)
admin.site.register(Services, ServicesAdmin)