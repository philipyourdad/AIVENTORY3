from django import forms
from django.contrib.auth.models import User

class SuperUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    is_superuser = forms.BooleanField(initial=True, required=False, label='Superuser')
    is_staff = forms.BooleanField(initial=True, required=False, label='Staff')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'is_superuser', 'is_staff')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'Passwords do not match')
        return cleaned_data 