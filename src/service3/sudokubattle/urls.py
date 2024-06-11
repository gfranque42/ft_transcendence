from django.urls import path, include
from . import views

urlpatterns = [
	path("sudoku", views.sudoku_board, name="sudoku_board")
]
