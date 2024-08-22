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


from .urls import CheckForTFA
from .models import UserProfile
from .forms import CreateUserForm, GetUserForm, Get2faForm, changeAvatar, changeUsername
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


import jwt, datetime, pyotp


class Profile(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'register/register.html'

    def get(self, request):
        formAvatar = changeAvatar()
        formUsername = changeUsername()
        print(request.headers)
        auth_header = request.headers.get('Authorization')
        print (auth_header)
        try: 
            print (auth_header)
            print ("\n\n\n\n\n")
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
            return render(request, "profile.html", {"formAvatar":formAvatar, "formUsername":formUsername})
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
    
    def patch(self, request):
        print (request.data)
        new_username = request.data['username']
        new_avatar = request.data['avatar']
        token = request.data['token']
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        userProfile = UserProfile.objects.get(id=decoded['id'])
        print ("\n\n\n\n\n")

        print (new_username)
        if new_username:
            print ("string is true")
            if User.objects.filter(username=new_username).exists():
                return Response({'detail': 'Username is taken'}, status=status.HTTP_401_UNAUTHORIZED)
            userProfile.user.username = new_username
            userProfile.user.save()
            # userProfile.save
        print (userProfile.user.username)
        if new_avatar:
            userProfile.avatar = new_avatar
            userProfile.save()
        
            
        
        return Response({'Success': 'No Verification'}, status=status.HTTP_200_OK)

        
# PATCH nothing is forced add it and save it some cgecks ie avatar 

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
            print("Check\n\n\n\n")
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

class RegisterForm(APIView):

    def get(self, request):
        form = CreateUserForm()
        print (form)
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
    print(userProfile.user.username)
    return Response({"Username": format(userProfile.user.username), "ID": format(userProfile.user.id)})
