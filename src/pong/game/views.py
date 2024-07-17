from django.shortcuts import render, HttpResponse

def home(request):
	return (render(request, "index.html"))

def index(request):
	return (render(request, "chat.html"))

def	room(request, room_name):
	return (render(request, "room.html", {"room_name": room_name}))
