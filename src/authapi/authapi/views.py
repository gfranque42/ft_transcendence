<<<<<<< HEAD
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import CreateUserForm
from .serializers import UserSerializer

@api_view(['POST'])
def login(request):
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
=======
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

@api_view(['POST'])
def login(request):
	user = get_object_or_404(User, username=request.data['username'])
	if not user.check_password(request.data['password']):
		return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
	token, created = Token.objects.get_or_create(user=user)
	serializer = UserSerializer(instance=user)
	return Response({"token": token.key, "user": serializer.data})


@api_view(['POST'])
def signup(request):
	serializer = UserSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		user = User.objects.get(username=request.data['username'])
		user.set_password(request.data['password'])
		user.save()
		token = Token.objects.create(user=user)
		return Response({"token": token.key, "user": serializer.data})
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
>>>>>>> 1542611 (✨ auth api: fonction plus qu'a implementer)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
<<<<<<< HEAD
    return Response({"message": "passed for {}".format(request.user.id)})
=======
	return Response("passed for {}".format(request.user.id))
>>>>>>> 1542611 (✨ auth api: fonction plus qu'a implementer)
