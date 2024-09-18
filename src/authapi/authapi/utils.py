from .serializers import  FriendRequestSerializer
from .models import  Friend_request
from .forms import AnswerFriendForm

from django.conf import settings
import json
from django.core.mail import send_mail
import pyotp, qrcode
from io import BytesIO
from django.http import HttpResponse
from sms import send_sms

import base64

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
