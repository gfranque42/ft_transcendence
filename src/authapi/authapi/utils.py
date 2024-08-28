
from django.conf import settings
import json
from django.core.mail import send_mail
import pyotp, qrcode
from io import BytesIO
from django.http import HttpResponse
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
        fail_silently=False,
    )




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

