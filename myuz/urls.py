from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('noveller/', include('noveller.urls')),
    path('api/', include('noveller.urls')),
    path('phusis/', include('phusis.urls')),
    path('api/', include('phusis.urls')),
    path('admin/', admin.site.urls),
]