
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
from django.conf.urls import handler404
import os

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'pages/static'),}),

    path('', TemplateView.as_view(template_name='pages/index.html'), name='base-home'),
    path('register/', TemplateView.as_view(template_name='pages/index.html'), name='register'),
    path('login/', TemplateView.as_view(template_name='pages/index.html'), name='login'),
    path('profile/', TemplateView.as_view(template_name='pages/index.html'), name='profile'),

    path('sudoku/', TemplateView.as_view(template_name='pages/index.html'), name='sudoku'),
    path('sudokubattle/<str:room_url>/', TemplateView.as_view(template_name='pages/index.html'), name='sudoku_lobby'),
    path('sudoku/waiting-room/', TemplateView.as_view(template_name='pages/index.html'), name='sudoku_waiting_room'),

    path('pong/', TemplateView.as_view(template_name='pages/index.html'), name='pong'),
    path('pong/<str:room_url>/', TemplateView.as_view(template_name='pages/index.html'), name='pong_lobby'),

    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),

]
handler404 = TemplateView.as_view(template_name='404.html')