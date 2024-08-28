from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie

from django.shortcuts import render, redirect

from django.http import JsonResponse    

from .urls import CheckForTFA
from .utils import generate_qr_code
from .models import UserProfile
from .forms import verificationEmail, verificationSMS, CreateUserForm, GetUserForm, Get2faForm, changeAvatar, changeUsername
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


import jwt, datetime, pyotp

class sendOTP(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
            if CheckForTFA(userProfile):
                return Response({'success': True})
            else :
                userProfile.tfa['email'] = False
                userProfile.tfa['app'] = False
                userProfile.tfa['sms'] = False
                return Response({'error': "User hasn't activated OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            

# !PHONE


# !PROFILE

class AddVerification(APIView):

    def post(self, request):
        token = request.data['token']
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        userProfile = UserProfile.objects.get(id=decoded['id'])

        formSMS = verificationSMS(request.data)
        formEmail = verificationEmail(request.data)
        formOTP = Get2faForm(request.data)
        if formSMS.is_valid() and formSMS.cleaned_data['phone_number']:
            userProfile.sms = formSMS.cleaned_data['phone_number']
            userProfile.tfa['sms'] = True
            userProfile.save()
            return JsonResponse({'success': True})

        elif formEmail.is_valid():
            userProfile.tfa['email'] = True
            userProfile.save()
            return JsonResponse({'success': True})

        elif formOTP.is_valid() and (formOTP.cleaned_data['otp']):
            totp = pyotp.TOTP(userProfile.otp_secret)
            if (totp.verify(formOTP.cleaned_data['otp'])):
                if (not userProfile.tfa['email'] and not userProfile.tfa['sms']):
                    userProfile.tfa['app'] = True
                return JsonResponse({'success': True})
            else:
                userProfile.tfa['email'] = False
                userProfile.tfa['app'] = False
                userProfile.tfa['sms'] = False
                return JsonResponse({'error': 'Wrong Code'}, status=400)

        return JsonResponse({'error': 'wromg input'}, status=400)




class Profile(APIView):

    def get(self, request):
        formAvatar = changeAvatar()
        formUsername = changeUsername()
        formEmail = verificationEmail()
        formSMS = verificationSMS()
        formOTP = Get2faForm()
        # print("here\n\n\n\n", formEmail)
        # print("here\n\n\n\n", formSMS)
        auth_header = request.headers.get('Authorization')
        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
            qr_code_base64 = generate_qr_code(userProfile)
            return render(request, "profile.html", {"formSMS":formSMS, "formEmail":formEmail, "formOTP":formOTP, "formAvatar":formAvatar, "formUsername":formUsername, 'qr_code_base64': qr_code_base64})
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
    
    def patch(self, request):
        new_username = request.data['username']
        new_avatar = request.data['avatar']
        token = request.data['token']
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        userProfile = UserProfile.objects.get(id=decoded['id'])

        if new_username:
            if User.objects.filter(username=new_username).exists():
                return Response({'error': 'Username is taken'}, status=status.HTTP_401_UNAUTHORIZED)
            userProfile.user.username = new_username
            userProfile.user.save()
            # userProfile.save
        if new_avatar:
            userProfile.avatar = new_avatar
            userProfile.save()
        return Response({'Success': 'No Verification'}, status=status.HTTP_200_OK)
        
# !VERIFICATION

class VerifyOTPView(APIView):
    def get(self, request):
        form = Get2faForm()
        auth_header = request.headers.get('Authorization')

        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
            if (CheckForTFA(userProfile)):
                return render(request, "2fa.html", {"form":form})
            # print(totp.now())
            # print("Check\n\n\n\n")
            return Response({'Success': 'No Verification'}, status=status.HTTP_200_OK)

            # print("Email verification sent")
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        form = Get2faForm(request.data)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user_id = form.cleaned_data['user_id']
            try:
                # print(user_id)
                user = User.objects.get(id=user_id)
                profile = UserProfile.objects.get(user=user)
                totp = pyotp.TOTP(profile.otp_secret)
                # print(totp.now())
                if totp.verify(otp):
                    return Response({'otp': 'Sucess'})
                else:
                    return Response({'otp': 'Verification Failed'})
            except User.DoesNotExist:
                return Response({'error': 'User not found.'})
        # print(form.errors)
        return Response({'error': 'Form invalid.', 'form':form.cleaned_data})        

# !LOGIN

class LoginForm(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'register/register.html'

    def get(self, request):
        form = GetUserForm()
        return render(request, "login.html", {"form":form})


    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            if not user.check_password(request.data['password']):
                return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)
            
            payload = {
                'id': user.id,
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=42),
                'iat': datetime.datetime.utcnow(),
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            serializer = UserSerializer(instance=user)
            return Response({"token": token, "user": serializer.data})
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"detail": "Username and password required."}, status=status.HTTP_400_BAD_REQUEST)

# !REGISTER

class RegisterForm(APIView):

    def get(self, request):
        form = CreateUserForm()
        # print (form)
        return render(request, "register.html", {"form":form})

    def post(self, request):
        form = CreateUserForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.data['password1'])  # Set the password correctly
            user.save()
            UserProfile.objects.create(user=user)
            payload = {
                'id': user.id,
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=42),
                'iat': datetime.datetime.utcnow(),
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')

            serializer = UserSerializer(instance=user)
            return Response({"token": token, "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'form': form.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def test_token(request):
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    userProfile = UserProfile.objects.get(id=payload['id'])
    # print(userProfile.user.username)
    return Response({"Username": format(userProfile.user.username), "ID": format(userProfile.user.id)})
