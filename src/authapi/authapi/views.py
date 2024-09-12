from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie

from django.db import IntegrityError

from django.shortcuts import render, redirect

from django.http import JsonResponse    

from .urls import CheckForTFA
from .utils import generate_qr_code
from .models import UserProfile, Friend_request
from .forms import verificationApp, verificationEmail, verificationSMS, CreateUserForm, GetUserForm, Get2faForm, changeAvatar, changeUsername
from .serializers import UserSerializer, FriendRequestSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


import jwt, datetime, pyotp



class FriendRequest(APIView):
    def post(self, request):
        from_user_id = request.data['from_user_id']
        to_user_id = request.data['to_user_id']
        try:
            from_user = UserProfile.objects.get(id=from_user_id)
            to_user = UserProfile.objects.get(id=to_user_id)
            friend_request = Friend_request(from_user=from_user, to_user=to_user)
            friend_request.save()
            return Response({'success': 'Invite sent'}, status=status.HTTP_201_CREATED)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'success': 'Invite already sent'}, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request):
        auth_header = request.headers.get('Authorization')
        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
            friend_requests = Friend_request.objects.filter(to_user=userProfile)
            serializer = FriendRequestSerializer(friend_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        from_user_id = request.data['from_user_id']
        to_user_id = request.data['to_user_id']
        try:
            from_user = UserProfile.objects.get(id=from_user_id)
            to_user = UserProfile.objects.get(id=to_user_id)
            friend_request = Friend_request.objects.filter(to_user=to_user, from_user=from_user)
            friend_request.delete()
            to_user.friends = from_user
            from_user.friends = to_user
            to_user.save()
            from_user.save()
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except friend_request.DoesNotExist:
            return Response({'error': 'friend request not found'}, status=status.HTTP_404_NOT_FOUND)



            



class sendOTP(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
            print("is verification on?")
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
        formApp = verificationApp(request.data)
        formOTP = Get2faForm(request.data)
        # print (formSMS.cleaned_data)
        if formSMS.is_valid() and formSMS.cleaned_data['phone_number']:
            print("65: ",formSMS.cleaned_data['phone_number'])
            userProfile.sms = formSMS.cleaned_data['phone_number']
            userProfile.tfa['sms'] = True
            userProfile.save()
            return JsonResponse({'success': True})
        elif formEmail.is_valid():
            userProfile.tfa['email'] = True
            userProfile.save()
            return JsonResponse({'success': True})

        elif formApp.is_valid() and formApp.cleaned_data['app']:
            print("75: ",formApp.cleaned_data['app'])
            userProfile.tfa['app'] = True
            return JsonResponse({'success': True})

        elif formOTP.is_valid() and (formOTP.cleaned_data['otp']):
            totp = pyotp.TOTP(userProfile.otp_secret)
            if (totp.verify(formOTP.cleaned_data['otp'])):
                return JsonResponse({'success': True})
            else:
                userProfile.tfa['email'] = False
                userProfile.tfa['app'] = False
                userProfile.tfa['sms'] = False
                return JsonResponse({'error': 'Wrong Code'}, status=400)

        return JsonResponse({'error': 'wromg input'}, status=400)




class Profile(APIView):

    def get(self, request):
        auth_header = request.headers.get('Authorization')
        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        initial_data = {'username': userProfile.user.username}

        formAvatar = changeAvatar()
        formUsername = changeUsername(initial=initial_data)
        formEmail = verificationEmail()
        formSMS = verificationSMS()
        formApp = verificationApp()
        formOTP = Get2faForm()
        # print("here\n\n\n\n", formEmail)
        # print("here\n\n\n\n", formSMS)
        qr_code_base64 = generate_qr_code(userProfile)
        return render(request, "profile.html", {"user": userProfile, "formApp":formApp, "formSMS":formSMS, "formEmail":formEmail, "formOTP":formOTP, "formAvatar":formAvatar, "formUsername":formUsername, 'qr_code_base64': qr_code_base64})
            
    
    def patch(self, request):
        formUsername = changeUsername(request.data)
        formAvatar = changeAvatar(request.data, request.FILES)
        token = request.data['token']
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        userProfile = UserProfile.objects.get(id=decoded['id'])
        # print(formUsername)
        # print(formAvatar)

        # new_avatar = formAvatar.cleaned_data['avatar']

        if formUsername.is_valid():
            new_username = formUsername.cleaned_data['username']
            if User.objects.filter(username=new_username).exists():
                return Response({'error': 'Username is taken'}, status=status.HTTP_401_UNAUTHORIZED)
            userProfile.user.username = new_username
            userProfile.user.save()
            # userProfile.save
        if formAvatar.is_valid():
            print("\n\n\n\n THIS IS NEW AVATAR ---------------------\n\n\n\n",request.FILES, "\n\n\n\n")
            userProfile.avatar = request.FILES["avatar"]
            userProfile.save()
        return Response({'success': 'No Verification'}, status=status.HTTP_200_OK)

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
            print("is verificatiom turned on?")
            if (CheckForTFA(userProfile)):
                return render(request, "2fa.html", {"form":form})
            # print(totp.now())
            # print("Check\n\n\n\n")
            return Response({'success': 'No Verification'}, status=status.HTTP_200_OK)

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
    return Response({"Username": format(userProfile.user.username), "ID": format(userProfile.user.id)})

@api_view(['GET'])
def test_OTP(request):
    print('Test\n\n\n\n')
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    userProfile = UserProfile.objects.get(id=payload['id'])
    print(userProfile.tfa)
    print(any(userProfile.tfa.values()))
    return Response({"method": any(userProfile.tfa.values())})
