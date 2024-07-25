from django.urls import path
from . import views

urlpatterns = [
	path('get/', views.getData),
	path('get/<str:pk>', views.getDetail),
	path('post/', views.postData),
	path('update/<str:pk>', views.updateData),
	path('delete/<str:pk>', views.deleteData),
]