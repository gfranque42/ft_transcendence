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


from .models import UserProfile
from .forms import CreateUserForm, GetUserForm, Get2faForm
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


import jwt, datetime, pyotp


class VerifyOTPView(APIView):
    def get(self, request):
        form = Get2faForm()
        auth_header = request.headers.get('Authorization')

        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
            totp = pyotp.TOTP(userProfile.otp_secret)
            
            # print("Email verification")
            # print(userProfile.otp_secret)
            # print(totp.now())
            send_mail(
                "Verifiaction",
                totp.now(),
                settings.EMAIL_HOST_USER,
                [userProfile.user.email],
                fail_silently=False,
            )
            # print(totp.now())

            # print("Email verification sent")
            return render(request, "2fa.html", {"form":form})
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
    return Response({"Username": format(userProfile.user.username), "ID": format(userProfile.user.id)})
