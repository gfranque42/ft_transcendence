from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Player
from .serializers import PlayerSerializer

@api_view(['GET'])
def	getData(request):
	players = Player.objects.all()
	serializer = PlayerSerializer(players, many=True)
	return (Response(serializer.data))

@api_view(['GET'])
def	getDetail(request, pk):
	players = Player.objects.get(username=pk)
	serializer = PlayerSerializer(players, many=False)
	return (Response(serializer.data))

@api_view(['POST'])
def	postData(request):
	serializer = PlayerSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return (Response(serializer.data))

@api_view(['POST'])
def	updateData(request, pk):
	player = Player.objects.get(username=pk)
	serializer = PlayerSerializer(instance=player, data=request.data)
	if serializer.is_valid():
		serializer.save()
	return (Response(serializer.data))

@api_view(['DELETE'])
def	deleteData(request, pk):
	player = Player.objects.get(username=pk)
	player.delete()
	return (Response('Player succesfully delete !'))
