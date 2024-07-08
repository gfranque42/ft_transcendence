from django.urls import re_path
from game import consumers

websocket_urlpatterns = [
	re_path(r'chat/$', consumers.PlayerConsumer.as_asgi()),
]
