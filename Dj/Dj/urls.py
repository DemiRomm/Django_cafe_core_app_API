from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/cafe_core_app/', include('cafe_core_app.urls')),
    path('admin/', admin.site.urls),
]
