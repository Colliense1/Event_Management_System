from os import name
from django import forms
from django.contrib.auth.models import User
from .models import UserRegistrationModel, Event

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = UserRegistrationModel
        fields = ['full_name', 'username', 'email', 'phone_number', 'password',  'profile_photo', 'gender', 'address']

        widgets = {
            'address': forms.TextInput(attrs={'size': '150'}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )
        user_pro = super().save(commit=False)
        user_pro.user = user
        if commit:
            user_pro.save()
        return user_pro 

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'location', 'description', 'max_attendees']

        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }