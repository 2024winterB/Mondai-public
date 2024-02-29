from django.contrib import admin
from django.urls import path, include

#追加
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_control

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mondai/', include('Mondai_app.urls')),
    #追加
    path('mondai/login/sw.js', (TemplateView.as_view(template_name="sw.js",
    content_type='application/javascript', )), name='sw.js'),
]
