from django.shortcuts import render, HttpResponse

def home(request):
	return (render(request, "pong_game/index.html"))
