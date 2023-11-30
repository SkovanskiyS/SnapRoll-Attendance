from django import forms
from .models import Students


class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        # fields = '__all__' #add all fields to db
        fields = (
            'username', 'password', 'f_name', 'l_name', 'm_name', 'enroll_number', 'faculty', 'semester', 'section',
            'face')
        widgets = {
            'password': forms.PasswordInput()
        }
