from django.urls import path, re_path
from django.views.generic import TemplateView

urlpatterns = [
<<<<<<< HEAD
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='pages/index.html'), name='base-home'),
=======
    # path('api/', api.home   , name='base-home'),
<<<<<<< HEAD
    path('', views.home, name="base-home"),
    path('login/', views.login, name="base-login"),
    path('signup/', views.signup, name="base-signup"),

>>>>>>> 9be107d (✨ feat: SAP working)
]
=======
    # path('', views.home, name="base-home"),
	# re_path(r'^(?:.*)/?$', name="base-home"),
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='pages/index.html'), name='base-home'),
]
>>>>>>> 8854aa9 (🚧 authentication: combined with pages)
