from typing import Any
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Friend_request
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.utils.safestring import mark_safe
from django import forms

import jwt, pyotp


class SVGFileInput(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        # Define the SVG markup that acts as the clickable upload area
        svg_markup = '''
        <label for="id_avatar" style="cursor: pointer;">
            <svg class="avatar-modify" width="19" height="19" viewBox="0 0 19 19" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M13.4837 0.790801C14.5455 -0.263603 16.267 -0.263603 17.3288 0.790819L17.4841 0.945223C18.5459 1.99964 18.5459 3.70919 17.4841 4.7636L11.1404 11.0636C10.6306 11.57 9.93904 11.8544 9.21799 11.8544H7.25C6.7495 11.8544 6.34375 11.4515 6.34375 10.9544V9.00001C6.34375 8.28391 6.6302 7.59716 7.14005 7.09082L13.4837 0.790801ZM16.0471 2.0636C15.6932 1.71213 15.1193 1.71213 14.7654 2.0636L14.4222 2.40443L15.8594 3.83163L16.2025 3.49082C16.5565 3.13933 16.5565 2.56949 16.2025 2.21802L16.0471 2.0636ZM14.5778 5.10441L13.1406 3.67721L8.42169 8.3636C8.25173 8.53238 8.15625 8.76131 8.15625 9.00001V10.0544H9.21799C9.45833 10.0544 9.68884 9.95959 9.8588 9.79082L14.5778 5.10441Z" fill="black"/>
            <path d="M0 4.65435C0 3.16317 1.21722 1.95435 2.71875 1.95435H7.25C7.7505 1.95435 8.15625 2.35729 8.15625 2.85435C8.15625 3.3514 7.7505 3.75435 7.25 3.75435H2.71875C2.21825 3.75435 1.8125 4.15729 1.8125 4.65435V15.4543C1.8125 15.9513 2.21825 16.3543 2.71875 16.3543H13.5938C14.0942 16.3543 14.5 15.9513 14.5 15.4543V10.9543C14.5 10.4573 14.9058 10.0543 15.4062 10.0543C15.9067 10.0543 16.3125 10.4573 16.3125 10.9543V15.4543C16.3125 16.9455 15.0952 18.1543 13.5938 18.1543H2.71875C1.21722 18.1543 0 16.9455 0 15.4543V4.65435Z" fill="black"/>
        </label>
        <input type="file" name="avatar" accept="image/*" id="id_avatar" class="file-input" style="display:none;">
        '''
        return mark_safe(svg_markup)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control form-username', 'placeholder': 'Username', 'autocomplete': 'username'}),
            "email": forms.EmailInput(attrs={'class': 'form-control form-email', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control form-password-1', 'placeholder': 'Password', 'autocomplete': 'new-password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control form-password-2', 'placeholder': 'Password confirmation', 'autocomplete': 'new-password'})
        # self.fields.pop('usable_password')
        # print(self.fields) 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError('Enter a valid email address.')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with that email already exists.')
        else:
            raise forms.ValidationError('Email field is required.')
        # print(email)
        return email


class GetUserForm(forms.Form):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'current-password'}))

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
    avatar = forms.ImageField(required=False, widget=SVGFileInput())



class changeUsername(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'profile-username-field'}),
        label='Username',
        )
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Username already exists.')
        return username


class verificationEmail(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-email', 'placeholder': 'Email'}))
    token = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        token = cleaned_data.get('token')
        print("clening to verify email")
        if email and token:
            try:
                # Decode the token to get user ID
                decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
                user_id = decoded['id']
                cleaned_data['user_id'] = user_id
                userProfile = UserProfile.objects.get(id=user_id)
                
                # Verify the email
                if userProfile.user.email!= email:
                    raise forms.ValidationError('Email not verified')
            except jwt.ExpiredSignatureError:
                raise forms.ValidationError('Token has expired')
            except jwt.InvalidTokenError:
                raise forms.ValidationError('Invalid token')
            except UserProfile.DoesNotExist:
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

        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            cleaned_data['phone_number'] = False
            return cleaned_data
            # raise forms.ValidationError("No Number giver.")


        
        # Remove non-numeric characters
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        # Check and format the phone number
        if len(phone_number) == 10 and phone_number.startswith('0'):
            cleaned_data['phone_number'] = '+33' + phone_number
        elif len(phone_number) == 9:
            cleaned_data['phone_number'] = '+330' + phone_number
        else:
            raise forms.ValidationError("Enter a valid French phone number.")
        return cleaned_data 

class verificationApp(forms.Form):
    app = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must accept check the box.'}
    )

# class verificationAPP(forms.Form):


    # def __init__(self, *args, **kwargs):
    #     super(CreateUserForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['placeholder'] = 'Username'
    #     self.fields['password1'].widget.attrs['placeholder'] = 'Password'
    #     self.fields['password2'].widget.attrs['placeholder'] = 'Password confirmation'
class SendFriendForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput(), required=True)
    to_user = forms.UUIDField(required=True, widget=forms.TextInput(attrs={'placeholder': "Enter a friend's code", 'class': 'form-control form-friend'}))
    
    def clean(self):
        cleaned_data = super().clean()

        token = cleaned_data.get('token')
        try:
            to_user = UserProfile.objects.get(uuid=cleaned_data['to_user'])
        except:
            raise forms.ValidationError("User not found.")

        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        from_user_id = decoded['id']
        
        cleaned_data['from_user_id'] = from_user_id
        cleaned_data['to_user_id'] = to_user.id

        return cleaned_data


class AnswerFriendForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput(), required=True)
    from_user_id = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()


        token = cleaned_data.get('token')
        try:
            to_user = UserProfile.objects.get(id=cleaned_data['from_user_id'])
        except:
            raise forms.ValidationError("User not found.")

        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        from_user_id = decoded['id']
        
        cleaned_data['from_user_id'] = from_user_id
        cleaned_data['to_user_id'] = to_user.id

        return cleaned_data

