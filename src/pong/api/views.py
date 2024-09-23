from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Player, Room
from .serializers import PlayerSerializer, RoomSerializer
import os
from django.shortcuts import render
from django.http import JsonResponse

@api_view(['GET'])
def	getPlayer(request):
	players = Player.objects.all()
	serializer = PlayerSerializer(players, many=True)
	return (Response(serializer.data))

@api_view(['GET'])
def	getPlayerDetail(request, pk):
	players = Player.objects.get(username=pk)
	serializer = PlayerSerializer(players, many=False)
	return (Response(serializer.data))

@api_view(['POST'])
def	postPlayer(request):
	serializer = PlayerSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return (Response(serializer.data))
	return Response(serializer.errors, status=400)

@api_view(['POST'])
def	updatePlayer(request, pk):
	player = Player.objects.get(username=pk)
	serializer = PlayerSerializer(instance=player, data=request.data)
	if serializer.is_valid():
		serializer.save()
		return (Response(serializer.data))
	return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def	deletePlayer(request, pk):
	player = Player.objects.get(username=pk)
	player.delete()
	return (Response('Player succesfully delete !'))

@api_view(['GET'])
def	getRoom(request):
	rooms = Room.objects.all()
	serializer = RoomSerializer(rooms, many=True)
	return (Response(serializer.data))

@api_view(['GET'])
def	getRoomDetail(request, pk):
	rooms = Room.objects.get(url=pk)
	serializer = RoomSerializer(rooms, many=False)
	return (Response(serializer.data))

@api_view(['POST'])
def	postRoom(request):
	serializer = RoomSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return (Response(serializer.data))
	print(serializer.is_valid())
	print(serializer.errors)
	print(serializer.data)
	print(request.data)
	return Response(serializer.errors, status=400)

@api_view(['POST'])
def	updateRoom(request, pk):
	room = Room.objects.get(url=pk)
	serializer = RoomSerializer(instance=room, data=request.data)
	if serializer.is_valid():
		serializer.save()
		return (Response(serializer.data))
	return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def	deleteRoom(request, pk):
	room = Room.objects.get(url=pk)
	room.delete()
	return (Response('Room succesfully delete !'))

@api_view(['GET'])
def	getIndex(request):
	return (render(request, "index.html"))

@api_view(['GET'])
def	getLobby(request, pk):
	# room_name = request.headers.get["room_name"]
	return (render(request, "pong.html", {"room_name": pk}))

def	test(request):
	data = {'status': 'ok'}
	return JsonResponse(data)
