from rest_framework import serializers
from .models import Player

class	PlayerSerializer(serializers.HyperlinkedModelSerializer):
	class	Meta:
		model = Player
		fields = ['username', 'game_played', 'game_wined']
# fields = '__all__' can work
