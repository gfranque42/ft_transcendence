from django.shortcuts import render, HttpResponse
from django.http import Http404
from .models import Bob, Player
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PlayerSerializer

def home(request):
	return (render(request, "index.html"))

def chat(request):
	return (render(request, "chat.html"))

def	loby(request, gamemode):
	return (render(request, "pong.html", {"gamemode": gamemode}))

def	room(request, room_name):
	return (render(request, "room.html", {"room_name": room_name}))

def bob(request):
	try:
		bob = Bob.objects.get(name="bob")
	except Bob.DoesNotExist:
		raise Http404("Bob not found")
	bob.refreshtime += 1
	bob.objects.save()# a continuer
	return (render(request, "index.html"))

@api_view(['GET'])
def	getData(request):
	players = Player.objects.all()
	serializer = PlayerSerializer(players, many=True)
	return Response(serializer.data)

@api_view(['POST'])
def	postData(request):
	serializer = PlayerSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)
