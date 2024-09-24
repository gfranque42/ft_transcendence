from .serializers import  FriendRequestSerializer
from .models import  Friend_request
from .forms import AnswerFriendForm

from django.conf import settings
import json, datetime, pyotp, qrcode, base64, jwt

from jwt import ExpiredSignatureError, InvalidTokenError

from django.core.mail import send_mail
from io import BytesIO
from django.http import HttpResponse
from sms import send_sms

import base64
from .models import UserProfile, Friend_request, GameHistory

from django.contrib.sessions.models import Session
from django.utils import timezone


def most_common(lst):
    return max(set(lst), key=lst.count)

def gameStats(user):
    total_games = user.games()

    won_games = user.games_won.all()

    games_played_count = len(total_games)
    games_won_count = len(won_games)
    if (len(total_games) == 0) :
        win_ratio = 0
        rival = None
    else:
        print("\n\n\n\n", total_games, "\n\n\n\n")
        win_ratio = (len(won_games) / len(total_games))
        opponents = []
        for game in total_games:
            if game.winner == user:
                opponents.append(game.loser)
            else:
                opponents.append(game.winner)
        rival = most_common(opponents)

    games_lost_count = (games_played_count - games_won_count)

    return_objects = [{
            "games_played": games_played_count,
            "games_won": games_won_count,
            "games_lost": games_lost_count,
            "win_ratio": win_ratio,
            "rival": {"user": rival, "is_logged_in": CheckToken(rival)}}]

    return return_objects

     


def CheckToken(user):
    if (not user):
        return False
    token = user.jwt
    try:
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        UserProfile.objects.get(id=decoded['id'])
        print("\n\n\n\n this i happening in chectoken \n\n\n\n\n")
        return True    
    except jwt.ExpiredSignatureError:
        # The token has expired
        return False

    except jwt.InvalidTokenError:
        # The token is invalid (wrong signature, wrong secret, malformed token, etc.)
        return False


def CreateToken(userProfile):
    user = userProfile.user
    payload = {
        'id': user.id,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=2),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    userProfile.jwt = token
    userProfile.save()
    return (token)

def JsonItieator(json_data):
    for key, value in json_data.items():
        if (value == True):
            return key
    return None

def SendOTPbyEmail(userProfile):
    totp = pyotp.TOTP(userProfile.otp_secret)
    send_mail(
        "Verifiaction",
        totp.now(),
        settings.EMAIL_HOST_USER,
        [userProfile.user.email],
        fail_silently=False
    )
    print("email sent")




def generate_qr_code(userProfile):
    # Replace 'YourApp' with your app name and 'user@example.com' with the user's email
    totp = pyotp.TOTP(userProfile.otp_secret)
    uri = totp.provisioning_uri(userProfile.user.email, issuer_name="Ft_transcendance")

    # Generate the QR code
    qr = qrcode.make(uri)
    img_io = BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    
    img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
    
    return img_base64


def SendOTPbySMS(userProfile):
    totp = pyotp.TOTP(userProfile.otp_secret)
    print(userProfile.sms)
    send_sms(
        "Verifiaction",
        totp.now(),
        settings.SMS_HOST_USER,
        [userProfile.sms],
        # fail_silently=False
    )


def SendOTPbyApp(userProfile):
    return True


def CheckForTFA(userprofile):
    print("Checking for TFA...")
    return_value = False
    otp_methods = {
        'email': SendOTPbyEmail,
        'sms': SendOTPbySMS,
        'app': SendOTPbyApp,
    }
    methode = JsonItieator(userprofile.tfa)
    if (methode):
        otp_methods[methode](userprofile)
        print(methode)
        return_value = True
    return return_value

def GetFriendRequests(userProfile):
    friend_requests = Friend_request.objects.filter(to_user=userProfile)
    serializer = FriendRequestSerializer(friend_requests, many=True)
    return serializer.data
