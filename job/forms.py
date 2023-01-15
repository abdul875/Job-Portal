from django import forms
from django.forms import ModelForm

from .models import *


class JobPostingForm(ModelForm):
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )  # image
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))  # date of birth
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))  # last donation

    class Meta:
        model = Job  # JobModel
        fields = '__all__'  # all fields
        exclude = ['recruiter', 'creationdate']  # exclude user
