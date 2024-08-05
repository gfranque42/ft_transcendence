# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/sudokubattle/(?P<room_name>\w+)/$", consumers.SudokuConsumer.as_asgi()),
]
