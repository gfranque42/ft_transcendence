from django.urls import path
from . import views

urlpatterns = [
	path('getplayer/', views.getPlayer),
	path('getplayer/<str:pk>', views.getPlayerDetail),
	path('postplayer/', views.postPlayer),
	path('updateplayer/<str:pk>', views.updatePlayer),
	path('deleteplayer/<str:pk>', views.deletePlayer),
	path('getroom/', views.getRoom),
	path('getroom/<str:pk>', views.getRoomDetail),
	path('postroom/', views.postRoom),
	path('updateroom/<str:pk>', views.updateRoom),
	path('deleteroom/<str:pk>', views.deleteRoom),
]
