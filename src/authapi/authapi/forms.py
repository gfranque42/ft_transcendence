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
        # print(self.fields) 

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


class changeAvatar(forms.Form):
    avatar = forms.ImageField(required=False)



class changeUsername(forms.Form):
    username = forms.CharField(required=False)



class verificationEmail(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-email', 'placeholder': 'Email'}))
    token = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        token = cleaned_data.get('token')
        print("\n\n\n\nclening to verify email\n\n\n\n")
        if email and token:
            try:
                # Decode the token to get user ID
                decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
                user_id = decoded['id']
                cleaned_data['user_id'] = user_id
                userProfile = UserProfile.objects.get(id=user_id)
                
                # Verify the email
                if userProfile.user.email!= email:
                    print("\n\n1\n\n")
                    raise forms.ValidationError('Email not verified')
            except jwt.ExpiredSignatureError:
                print("\n\n2\n\n")
                raise forms.ValidationError('Token has expired')
            except jwt.InvalidTokenError:
                print("\n\n3\n\n")
                raise forms.ValidationError('Invalid token')
            except UserProfile.DoesNotExist:
                print("\n\n4\n\n")
                raise forms.ValidationError('User not found')
        print("finished verifying email")
        return cleaned_data


class verificationSMS(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput(), required=True) 
    phone_number = forms.CharField(
        max_length=10,  
        widget=forms.TextInput(attrs={'placeholder': 'Enter French phone number', 'class': 'phone_number_form'}),
        label="Phone Number",
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()

        print (cleaned_data)
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            cleaned_data['phone_number'] = False
            return cleaned_data
            # raise forms.ValidationError("No Number giver.")


        
        # Remove non-numeric characters
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        # Check and format the phone number
        if len(phone_number) == 10 and phone_number.startswith('0'):
            cleaned_data['phone_number'] = '+33' + phone_number[1:] 
        elif len(phone_number) == 9:
            cleaned_data['phone_number'] = '+33' + phone_number
        else:
            raise forms.ValidationError("Enter a valid French phone number.")
        return cleaned_data 



# class verificationAPP(forms.Form):


    # def __init__(self, *args, **kwargs):
    #     super(CreateUserForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['placeholder'] = 'Username'
    #     self.fields['password1'].widget.attrs['placeholder'] = 'Password'
    #     self.fields['password2'].widget.attrs['placeholder'] = 'Password confirmation'

