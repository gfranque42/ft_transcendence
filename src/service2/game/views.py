from django.shortcuts import render, HttpResponse
from .models import Player

def pong(request):
	ply = Player.objects.all()
	if (ply):
		return (render(request, "pong_game/index.html", {"ply": ply}))
