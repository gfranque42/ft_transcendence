# urls.py
from django.urls import path
from . import views

urlpatterns = [
	path('sudokubattle/', views.home, name='home'),
	path('sudokubattle/<str:room_url>/', views.sudoku_board, name='sudoku_board'),
	path('sudokubattle/api/sudoku/create/', views.check_or_create_sudoku_room, name='create_sudoku_room'),
]
