from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('phusis/', include('phusis.urls')),
    path('noveller/', include('noveller.urls')),
    # path('api/', include('noveller.urls'), include('phusis.urls')),
    path('admin/', admin.site.urls),
]