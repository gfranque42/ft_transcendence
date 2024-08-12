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
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import CreateUserForm, GetUserForm
from .serializers import UserSerializer


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
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(instance=user)
            return Response({"token": token.key, "user": serializer.data})
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"detail": "Username and password required."}, status=status.HTTP_400_BAD_REQUEST)

class RegisterForm(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'register/register.html'

    def get(self, request):
        form = CreateUserForm()
        return render(request, "register.html", {"form":form})

    def post(self, request):
        form = CreateUserForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.data['password1'])  # Set the password correctly
            user.save()
            token = Token.objects.create(user=user)
            serializer = UserSerializer(instance=user)
            return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'form': form.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"Username": format(request.user.username)})
