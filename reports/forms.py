from crispy_forms.layout import Layout
from django.db.models import fields
from django.utils.safestring import mark_safe
from inventory.models import ItemCategory
from inventory.models import ItemCategory, Item
from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.db import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row,Field
from crispy_forms.bootstrap import AppendedText, PrependedText, PrependedAppendedText


class SearchBetweenTwoDatesForm(forms.Form):
    start_date_time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],widget = forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local'}, format = '%Y-%m-%dT%H:%M'))
    end_date_time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],widget = forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local'}, format = '%Y-%m-%dT%H:%M'))
