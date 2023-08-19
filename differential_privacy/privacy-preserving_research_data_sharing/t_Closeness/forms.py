from django import forms
from general.forms import AbstractForm
from django.utils.translation import gettext

class ParameterForm(AbstractForm):
    k = forms.IntegerField(label='K', initial=2, min_value=1, help_text=gettext('去識別化後，在任意查詢條件下，至少會同時查到K筆資料'))