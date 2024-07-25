from django.urls import path
from . import views

urlpatterns = [
	path("", views.home, name="home"),
	# path("", views.chat, name="chat"),
	path("bob/", views.bob, name="bob"),
	path("chat/<str:room_name>/", views.room, name="room"),
]
