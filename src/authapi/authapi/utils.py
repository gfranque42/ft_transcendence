
from django.conf import settings
import json
from django.core.mail import send_mail
import pyotp


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
        fail_silently=False,
    )

# def SendOTPbySMS(userProfile):


# def SendOTPbyApp(userProfile):


def CheckForTFA(userprofile):
    otp_methods = {
        'email': SendOTPbyEmail,
        # 'sms': SendOTPbySMS,
        # 'app': SendOTPbyApp,
    }
    methode = JsonItieator(userprofile.tfa)
    if (methode):
        otp_methods[methode](userprofile)
        return True
    return False    

