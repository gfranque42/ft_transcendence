from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django import forms

import jwt, pyotp


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control form-username', 'placeholder': 'Username'}),
            "email": forms.EmailInput(attrs={'class': 'form-control form-email', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control form-password-1', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control form-password-2', 'placeholder': 'Password confirmation'})
        # self.fields.pop('usable_password')
        print(self.fields) 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Enter a valid email address.')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with that email already exists.')
        else:
            raise forms.ValidationError('Email field is required.')
        # print(email)
        return email


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

class Get2faForm(forms.Form):
    otp = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    token = forms.CharField(widget=forms.HiddenInput(), required=True) 
    def clean(self):
        cleaned_data = super().clean()
        otp = cleaned_data.get('otp')
        token = cleaned_data.get('token')

        if otp and token:
            try:
                # Decode the token to get user ID
                decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
                user_id = decoded['id']
                cleaned_data['user_id'] = user_id
                userProfile = UserProfile.objects.get(id=user_id)
                
                # Verify the OTP
                totp = pyotp.TOTP(userProfile.otp_secret)
                # print(userProfile.otp_secret)
                # print(totp.now())
                if not totp.verify(otp):
                    raise forms.ValidationError('Invalid OTP')
            except jwt.ExpiredSignatureError:
                raise forms.ValidationError('Token has expired')
            except jwt.InvalidTokenError:
                raise forms.ValidationError('Invalid token')
            except UserProfile.DoesNotExist:
                raise forms.ValidationError('User not found')
        return cleaned_data


class ChangeAvatar(forms.Form):
    avatar = forms.ImageField(upload_to="images/", blank=True, null=True)
    username = forms.CharField(max_length=254, unique=True)

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


