from django.contrib import admin
from django.urls import re_path, path
from authapi.utils import CheckForTFA
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
import os

urlpatterns = [
    re_path(r'^auth/static/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'authapi/static'),}),
    re_path(r'^auth/media/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'media/'),}),

	path("admin/", admin.site.urls),
    re_path(r'^auth/login$', views.LoginForm.as_view(), name='login'),
    re_path(r'^auth/logout$', views.LogOut.as_view(), name='logout'),
    re_path(r'^auth/register$', views.RegisterForm.as_view(), name='register'), 
    re_path(r'^auth/verification$', views.VerifyOTPView.as_view(), name='verification'), 
    re_path(r'^auth/test_token$', views.test_token, name='test_token'),
    re_path(r'^auth/get_token$', views.get_token, name='get_token'),
    re_path(r'^auth/test_OTP$', views.test_OTP, name='test_OTP'),
    re_path(r'^auth/profile$', views.Profile.as_view(), name='profile'),
    re_path(r'^auth/verification-add$', views.AddVerification.as_view(), name='addVerification'), 
    re_path(r'^auth/send-otp$', views.sendOTP.as_view(), name='sendOTP'),  
    re_path(r'^auth/send-friend-request$', views.FriendRequest.as_view(), name='sendFriendRequest'),  
    re_path(r'^auth/friends$', views.Friend.as_view(), name='Friends'),
    re_path(r'^auth/user-status$', views.UserStatus.as_view(), name='UserStatus'),
    re_path(r'^auth/games$', views.Games.as_view(), name='games'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# {
#     'id': 1,
#     'from_user': 
#         {
#             'user': 
#                 {
#                     'id': 1,
#                     'username': 'stn',
#                     'email': 'baneg2335@eixdeal.com'
#                 }
#             'avatar': '/media/images/default_avatar.jpg'}, 'to_user': 2}
