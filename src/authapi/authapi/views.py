from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import IntegrityError

import base64

from django.shortcuts import render

from django.http import JsonResponse    


from django.contrib.auth import authenticate, login

from .urls import CheckForTFA
from .utils import generate_qr_code, GetFriendRequests, gameStats, CreateToken, CheckToken
from .models import UserProfile, Friend_request, GameHistory
from .forms import SendFriendForm, verificationApp, verificationEmail, verificationSMS, CreateUserForm, GetUserForm, Get2faForm, changeAvatar, changeUsername
from .serializers import UserSerializer, FriendRequestSerializer, GamesSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from django.middleware.csrf import get_token
# from jwt import ExpiredSignatureError, InvalidTokenError


import jwt, pyotp, json


# !GAMES

class Games(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        try:
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            # You might want to check if the user exists here, based on your application logic
            UserProfile.objects.get(id=user_id)  # Ensure to handle potential DoesNotExist exception
            
            # Instead of getting CSRF_COOKIE from META, retrieve it from cookies
            csrf_token = request.COOKIES.get('csrftoken')  # Default name is 'csrftoken'

            return Response({'csrf_token': csrf_token}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
    def post(self, request):
        winner_id = request.data['winner_id']
        loser_id = request.data['loser_id']
        score_winner = request.data['score_winner']
        score_loser = request.data['score_loser']
        game_type = request.data['game_type']
        try :
            winner = UserProfile.objects.get(id=winner_id)
            loser = UserProfile.objects.get(id=loser_id)
            game_history = GameHistory.objects.create(winner=winner,
                                                     loser=loser,
                                                      score_winner=score_winner,
                                                      score_loser=score_loser,
                                                      game_type=game_type)
            print (game_history)
            game_history.save()
            serializer = GamesSerializer(game_history)

            return Response({'success': 'Game history created', 'history': serializer.data}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
 

# !USER

class UserStatus(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        try:
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            user = UserProfile.objects.get(id=user_id)
            user.status = not user.status
            user.save()
            return Response({'success': 'Status changed'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)



# !FRIEND

class Friend(APIView):
    def delete(self, request):
        auth_header = request.headers.get('Authorization')
        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            friend_id = request.data.get('friend_id')
            friend = UserProfile.objects.get(id=friend_id)
            user = UserProfile.objects.get(id=user_id)
            user.friends.remove(friend)
            friend.friends.remove(user)
            return Response({'Succes': "You lost a friend :'("}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)


class FriendRequest(APIView):
    def post(self, request):
        formFriend = SendFriendForm(request.data)
        if not formFriend.is_valid():
            return Response(formFriend.errors, status=status.HTTP_400_BAD_REQUEST)
        print(formFriend)
        from_user_id = formFriend.cleaned_data['from_user_id']
        to_user_id = formFriend.cleaned_data['to_user_id']
        if (to_user_id == from_user_id):
            return Response({'success': 'Find friends'}, status=status.HTTP_201_CREATED)
        try:
            from_user = UserProfile.objects.get(id=from_user_id)
            to_user = UserProfile.objects.get(id=to_user_id)
            if (to_user.friends.filter(id=from_user_id).exists()):
                return Response({'success': 'Already Friends'}, status=status.HTTP_400_BAD_REQUEST)
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

        data = json.loads(request.body)
        from_user_id = data.get('from_user_id')
        token = data.get('token')
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        to_user = UserProfile.objects.get(id=decoded['id'])
        try:
            from_user = UserProfile.objects.get(id=from_user_id)
            friend_request = Friend_request.objects.filter(to_user=to_user, from_user=from_user)
            friend_request.delete()
            to_user.friends.add(from_user)
            from_user.friends.add(to_user)
            to_user.save()
            from_user.save()
            return Response({'success': 'Friend request accepted'}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except friend_request.DoesNotExist:
            return Response({'error': 'friend request not found'}, status=status.HTTP_404_NOT_FOUND)
  
    def delete(self, request):
        from_user_id = request.data['from_user_id']
        token = request.data['token']
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        to_user = UserProfile.objects.get(id=decoded['id'])
        try:
            from_user = UserProfile.objects.get(id=from_user_id)
            friend_request = Friend_request.objects.filter(to_user=to_user, from_user=from_user)
            friend_request.delete()
            to_user.save()
            from_user.save()
            return Response({'success': 'Friend request deleted'}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except friend_request.DoesNotExist:
            return Response({'error': 'friend request not found'}, status=status.HTTP_404_NOT_FOUND)



            

DICT = {
    "sms": False,
    "email": False,
    "app": False,
}




class sendOTP(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
            
            for item in DICT:
                if (DICT[item]):
                    userProfile.tfa[item] = DICT[item]
            if CheckForTFA(userProfile):
                return Response({'success': True})
            else :
                userProfile.tfa['email'] = False
                userProfile.tfa['app'] = False
                userProfile.tfa['sms'] = False
                return Response({'error': "User hasn't activated OTP"}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



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
        print ("User profile tfa: ", userProfile.tfa)
        print("\n\n\n")
        if formOTP.is_valid() and (formOTP.cleaned_data['otp']):
            print("User profile otp: ", formOTP.cleaned_data['otp'])
            totp = pyotp.TOTP(userProfile.otp_secret)
            if (totp.verify(formOTP.cleaned_data['otp'])):
                for item in DICT:
                    if (DICT[item]):
                        userProfile.tfa[item] = DICT[item]
                userProfile.save()
                return JsonResponse({'success': True, "otp": True})
            else:
                userProfile.tfa['email'] = False
                userProfile.tfa['app'] = False
                userProfile.tfa['sms'] = False
                return JsonResponse({'error': 'Wrong Code'}, status=400)

        print("OTPForm invalid: ", formOTP.cleaned_data)

        for item in DICT:
            DICT[item] = False

        if formSMS.is_valid() and formSMS.cleaned_data['phone_number']:
            print("65: ",formSMS.cleaned_data['phone_number'])
            userProfile.sms = formSMS.cleaned_data['phone_number']
            userProfile.save()
            DICT["sms"] = True
            for item in DICT:
                userProfile.tfa[item] = DICT[item]
            CheckForTFA(userProfile)
            return JsonResponse({'success': True, "otp": False})
        elif formEmail.is_valid():
            print("55: EMAIL:",userProfile.user.email)
            DICT['email'] = True
            for item in DICT:
                userProfile.tfa[item] = DICT[item]
            CheckForTFA(userProfile)
            return JsonResponse({'success': True, "otp": False})

        elif formApp.is_valid() and formApp.cleaned_data['app']:
            print("75: APP ACTIVATED")
            DICT['app'] = True
            for item in DICT:
                userProfile.tfa[item] = DICT[item]
            CheckForTFA(userProfile)
            return JsonResponse({'success': True, "otp": False})

        return JsonResponse({'error': 'wromg input'}, status=400)
    
    def delete(self, request):
        token = request.data['token']
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        userProfile = UserProfile.objects.get(id=decoded['id'])
        print("DATA:", request.data)
        if (request.data['sms']):
            print('Deleting sms')
            userProfile.tfa['sms'] = False
        elif (request.data['email']):
            print('Deleting email')
            userProfile.tfa['email'] = False
        elif (request.data['app']):
            print('Deleting app')
            userProfile.tfa['app'] = False
        else:
            print('Deleting none')

        userProfile.save()
        print('Checking 2fa: ', CheckForTFA(userProfile))
        return JsonResponse({'success': True})
    



class Profile(APIView):

    def get(self, request):
        print("Profile Get", flush=True)

        auth_header = request.headers.get('Authorization')
        if not auth_header :
            return Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        print("Profile Gett", flush=True)
        try: 
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        print("authentication", flush=True)        
        initial_data = {'username': userProfile.user.username}

        formAvatar = changeAvatar()
        formUsername = changeUsername(initial=initial_data)
        formEmail = verificationEmail()
        formSMS = verificationSMS()
        formApp = verificationApp()
        formOTP = Get2faForm()
        formSendFriend= SendFriendForm()
        friend_requests=GetFriendRequests(userProfile)
        qr_code_base64 = generate_qr_code(userProfile)

        # friends = userProfile.friends.all()

        # Create a list of friends with their login status
        friends_with_status = []
        for friend in userProfile.friends.all():
            is_logged_in = CheckToken(friend)  # Call the method here
            friends_with_status.append({
                'friend': friend,
                'is_logged_in': is_logged_in
            })
            # for userProfile_key, userProfile_value in friend_requests.items:
            
        return render(request, "profile.html", {"friend_requests": friend_requests,
                                                "user": userProfile,
                                                "formSendFriend": formSendFriend,
                                                "formApp":formApp,
                                                "formSMS":formSMS,
                                                "formEmail":formEmail,
                                                "formOTP":formOTP,
                                                "formAvatar":formAvatar,
                                                "formUsername":formUsername,
                                                'qr_code_base64': qr_code_base64,
                                                'friends': friends_with_status,
                                                "token": CreateToken(userProfile),
                                                "games": userProfile.games(),
                                                "stats": gameStats(userProfile)
                                                })
            
    
    def patch(self, request):
        formUsername = changeUsername(request.data)
        formAvatar = changeAvatar(request.data, request.FILES)
        try:
            token = request.data['token']



            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            userProfile = UserProfile.objects.get(id=decoded['id'])

            if formUsername.is_valid() and formUsername.cleaned_data['username'] and userProfile.user.username != formUsername.cleaned_data['username']:
                new_username = formUsername.cleaned_data['username']
                if User.objects.filter(username=new_username).exists():
                    return Response({'error': 'Username is taken'}, status=status.HTTP_401_UNAUTHORIZED)
                userProfile.user.username = new_username
                userProfile.user.save()
                # userProfile.save
            if formAvatar.is_valid() and formAvatar.cleaned_data["avatar"]:
                userProfile.avatar = formAvatar.cleaned_data["avatar"]
                userProfile.save()
            return Response({'success': 'No Verification'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)

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
                print(userProfile.tfa)
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


# !LOGOUT


class LogOut(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        print("logging out...")
        try:
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded['id']
            userProfile = UserProfile.objects.get(id=user_id)
            userProfile.jwt = "!".join(userProfile.jwt)
            userProfile.save()
            return Response({'Success': 'User logged out'}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token is expired'}, status=status.HTTP_404_NOT_FOUND)


# !LOGIN

class LoginForm(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'register/register.html'

    def get(self, request):
        form = GetUserForm()
        return render(request, "login.html", {"form":form})


    def post(self, request):
        try:
            user = authenticate(username=request.data['username'], password=request.data['password'])
            if not user:
                return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)
            login(request, user)
            userprofile = UserProfile.objects.get(user=user)
            serializer = UserSerializer(instance=user)
            return Response({"token": CreateToken(userprofile), "user": serializer.data})
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
            user = User.objects.create_user(form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password1"])
            user.save()
            userprofile = UserProfile.objects.create(user=user)

            serializer = UserSerializer(instance=user)
            return Response({"token": CreateToken(userprofile), "uuid": userprofile.uuid, "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'form': form.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_token(request):
    try:
        auth_header = request.headers.get('Authorization')
        if (not auth_header):
            return Response({"token": None}, status=status.HTTP_200_OK)
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        userProfile = UserProfile.objects.get(id=payload['id'])
        return Response({"token": CreateToken(userProfile) }, status=status.HTTP_201_CREATED)
    except jwt.ExpiredSignatureError:
        return Response({"token": None}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({"token": None}, status=status.HTTP_200_OK)

@api_view(['GET'])
def test_token(request):
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        userProfile = UserProfile.objects.get(id=payload['id'])
        return Response({"Username": format(userProfile.user.username), "ID": format(userProfile.user.id)})
    except jwt.ExpiredSignatureError:
        return Response({"expired": True}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({"token": None}, status=status.HTTP_200_OK)



@api_view(['GET'])
def test_OTP(request):
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        userProfile = UserProfile.objects.get(id=payload['id'])
        return Response({"method": any(userProfile.tfa.values())})
    except jwt.ExpiredSignatureError:
        return Response({"method": False}, status=status.HTTP_200_OK)
