from django.shortcuts import render
import os

# Create your views here.

def index(request):
	dns = {
		'dns': os.getenv('DNS'),
	}
	return (render(request, "index.html", dns))

def	pong(request, uri):
	return (render(request, "pong.html", {"uri": uri}))
