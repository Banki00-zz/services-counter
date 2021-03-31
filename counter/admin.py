from django.contrib import admin
from .models import *


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'pk', 'price', 'sum_for_worker','user', 'date_add')

    def get_title(self, obj):
        return obj.service.title

class TypeOfWorkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'fix_percent', 'user')


admin.site.register(TypeOfWork, TypeOfWorkAdmin)
admin.site.register(Services, ServicesAdmin)