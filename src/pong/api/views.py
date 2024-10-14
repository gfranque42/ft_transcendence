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

# @api_view(['GET'])
# def	getPlayer(request):
# 	players = Player.objects.all()
# 	serializer = PlayerSerializer(players, many=True)
# 	return (Response(serializer.data))

# @api_view(['GET'])
# def	getPlayerDetail(request, pk):
# 	players = Player.objects.get(username=pk)
# 	serializer = PlayerSerializer(players, many=False)
# 	return (Response(serializer.data))

# @api_view(['POST'])
# def	postPlayer(request):
# 	serializer = PlayerSerializer(data=request.data)
# 	if serializer.is_valid():
# 		serializer.save()
# 		return (Response(serializer.data))
# 	return Response(serializer.errors, status=400)

# @api_view(['POST'])
# def	updatePlayer(request, pk):
# 	player = Player.objects.get(username=pk)
# 	serializer = PlayerSerializer(instance=player, data=request.data)
# 	if serializer.is_valid():
# 		serializer.save()
# 		return (Response(serializer.data))
# 	return Response(serializer.errors, status=400)

# @api_view(['DELETE'])
# def	deletePlayer(request, pk):
# 	player = Player.objects.get(username=pk)
# 	player.delete()
# 	return (Response('Player succesfully delete !'))

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
		#create a new party
		gRoomsManager.rooms[request.data["url"]] = room(request.data["url"],
											request.data["maxPlayers"], request.data["difficulty"])
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
	template = loader.get_template('index.html')
	status: str = "bob"
	if gTournament.inTour == False and len(gTournament.lobbyRoom.players) == 0:
		status = "No tournament for now"
	elif gTournament.inTour == True:
		status = "Tournament in progress"
	else:
		status = str(gTournament.lobbyRoom.nbPlayers - len(gTournament.lobbyRoom.players))+" left to start"
	print("number of players waiting for the tournament: ",len(gTournament.lobbyRoom.players),flush=True)
	context = {
		'status': status,
	}
	return HttpResponse(template.render(context, request))
	# return (render(request, "index.html"))

@api_view(['GET'])
def	getLobby(request, pk):
	# room_name = request.headers.get["room_name"]
	return (render(request, "pong.html", {"room_name": pk}))

def	test(request):
	data = {'status': 'ok'}
	return JsonResponse(data)
