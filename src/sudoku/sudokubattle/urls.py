# urls.py
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('sudokubattle/<str:room_url>/', views.sudoku_board, name='sudoku_board'),
	path('api/sudoku/create/', views.create_sudoku_room, name='create_sudoku_room'),
]
