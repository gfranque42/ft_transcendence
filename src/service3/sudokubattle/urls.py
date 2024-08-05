# urls.py
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('sudokubattle/<str:room_name>/', views.sudoku_board, name='sudoku_board'),
]
