from django.forms import ModelForm, forms
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *


class TypeOfWorkForm(ModelForm):

    class Meta:
        model = TypeOfWork
        fields = '__all__'


class AddServiceForm(ModelForm):
    class Meta:
        model = AddService
        fields = ['price', 'service']
        labels = {
            'service': _('Услуга'),
            'price': _('Цена')
        }
