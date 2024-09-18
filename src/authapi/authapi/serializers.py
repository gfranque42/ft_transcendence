from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Friend_request


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