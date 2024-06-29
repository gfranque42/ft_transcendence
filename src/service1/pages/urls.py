from django.urls import path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    # path('api/', api.home   , name='base-home'),
    # path('', views.home, name="base-home"),
	# re_path(r'^(?:.*)/?$', name="base-home"),
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='pages/index.html'), name='base-home'),
]
