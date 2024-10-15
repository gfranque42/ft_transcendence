from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Room
from .serializers import RoomSerializer
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from app.consumers import gRoomsManager, gTournament
from app.rooms import room

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
		gRoomsManager.rooms[request.data["url"]] = room(request.data["url"],
											request.data["maxPlayers"], request.data["difficulty"])
		return (Response(serializer.data))
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
	template = loader.get_template('index.html')
	status: str = "bob"
	i = 0
	room = Room.objects.filter(difficulty=5)
	for rom in room:
		i += rom.playerCount
	if gTournament.players < 2:
		gTournament.players = gTournament.maxplayers
		gTournament.inTour = False
	if (gTournament.inTour == False and gTournament.players == gTournament.maxplayers and i == 0) or (gTournament.maxplayers - i) < 0:
		status = "No tournament for now"
	elif gTournament.inTour == True:
		status = "Tournament in progress"
	else:
		status = str(gTournament.maxplayers - i)+" left to start"
	context = {
		'status': status,
	}
	keys = []
	for key in gRoomsManager.rooms:
		if gRoomsManager.rooms[key].scoreL == 3 or gRoomsManager.rooms[key].scoreR == 3:
			gRoomsManager.rooms[key].endOfParty()
			keys.append(key)
	for i in keys:
		if i != "SbDaMcGf24":
			del gRoomsManager.rooms[i]
   
	return HttpResponse(template.render(context, request))

@api_view(['GET'])
def	getLobby(request, pk):
	return (render(request, "pong.html", {"room_name": pk}))

def	test(request):
	data = {'status': 'ok'}
	return JsonResponse(data)
