from django.shortcuts import render, HttpResponse

def pong(request):
	return (render(request, "pong_game/index.html"))
