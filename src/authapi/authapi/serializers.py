from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Friend_request, GameHistory


class UserSerializer(serializers.ModelSerializer):
	class Meta(object):
		model = User
		fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = UserProfile
		fields = ['user', 'avatar']

class FriendRequestSerializer(serializers.ModelSerializer):
	from_user = UserProfileSerializer()
	
	class Meta:
		model = Friend_request
		fields = ['id', 'from_user', 'to_user']

class GamesSerializer(serializers.ModelSerializer):

	class Meta:
		model = GameHistory
		fields = ['id', 'winner', 'loser', 'score_winner', 'score_loser', 'game_type', 'created_at']