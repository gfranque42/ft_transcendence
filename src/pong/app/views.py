from django.shortcuts import render
import os

# Create your views here.

# def index(request):
# 	dns = {
# 		'dns': os.getenv('DNS'),
# 	}
# 	return (render(request, "index.html", dns))

def	pong(request, room_name):
	return (render(request, "pong.html", {"room_name": room_name}))
