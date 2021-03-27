from django.contrib import admin
from .models import *
# Register your models here.


class AddServiceAdmin(admin.ModelAdmin):
    list_display = ('price', 'sum_for_worker', 'date_add')


class TypeOfWorkAdmin(admin.ModelAdmin):
    list_display = ('fix_percent',)


admin.site.register(TypeOfWork, TypeOfWorkAdmin)
admin.site.register(AddService, AddServiceAdmin)