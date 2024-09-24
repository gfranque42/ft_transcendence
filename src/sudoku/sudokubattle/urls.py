# urls.py
from django.urls import path
from . import views

urlpatterns = [
	path('sudokubattle/', views.home, name='home'),
	path('sudokubattle/<str:room_url>/', views.sudoku_board, name='sudoku_board'),
	path('sudokubattle/api/sudoku/create/', views.create_sudoku_room, name='create_sudoku_room'),
	path('sudokubattle/api/waiting_room/', views.waiting_room, name='waiting_room'),
]
