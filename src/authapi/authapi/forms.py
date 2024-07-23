from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control form-username', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control form-password-1', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control form-password-2', 'placeholder': 'Password confirmation'})

class GetUserForm(forms.Form):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username or password.")
        return cleaned_data


    # def __init__(self, *args, **kwargs):
    #     super(CreateUserForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['placeholder'] = 'Username'
    #     self.fields['password1'].widget.attrs['placeholder'] = 'Password'
    #     self.fields['password2'].widget.attrs['placeholder'] = 'Password confirmation'


