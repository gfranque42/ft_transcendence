from rest_framework import serializers
from app.models import Player, Room

class	PlayerSerializer(serializers.ModelSerializer):
	class	Meta:
		model = Player
		fields = '__all__'

class	RoomSerializer(serializers.ModelSerializer):
	class   Meta:
		model = Room
		fields = '__all__'

