from .serializers import  FriendRequestSerializer
from .models import  Friend_request

from django.conf import settings
import json, datetime, pyotp, qrcode, base64, jwt


from django.core.mail import send_mail
from io import BytesIO

import base64
from .models import UserProfile, Friend_request

import vonage


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
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=120),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    userProfile.jwt = token
    userProfile.save()
    return (token)

def JsonItieator(json_data):
    print ("printing json data :", json_data)
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

    client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
    response = client.sms.send_message({
        'from': settings.VONAGE_VIRTUAL_NUMBER,
        'to': [userProfile.sms],
        'text': totp.now(),
    })
    if response["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {response['messages'][0]['error-text']}")



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
    print ("printing json data :", userprofile.tfa)
    methode = JsonItieator(userprofile.tfa)
    for key, value in userprofile.tfa.items():
        if (value == True):
            otp_methods[key](userprofile)
    # print("methode :", methode)
    # if (methode):
        # print(methode)
    return_value = True

    return return_value

def GetFriendRequests(userProfile):
    friend_requests = Friend_request.objects.filter(to_user=userProfile)
    serializer = FriendRequestSerializer(friend_requests, many=True)
    return serializer.data
