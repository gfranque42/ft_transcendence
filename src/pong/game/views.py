from django.shortcuts import render, HttpResponse

def home(request):
	return (render(request, "index.html"))

def chat(request):
	return (render(request, "chat.html"))

def	loby(request, gamemode):
	return (render(request, "pong.html", {"gamemode": gamemode}))

def	room(request, room_name):
	return (render(request, "room.html", {"room_name": room_name}))
