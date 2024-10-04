
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
from django.conf.urls import handler404


urlpatterns = [
    # Home page: match "/"
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('', TemplateView.as_view(template_name='pages/index.html'), name='base-home'),

    # Catch-all for any other path to show 404
]
handler404 = TemplateView.as_view(template_name='404.html')