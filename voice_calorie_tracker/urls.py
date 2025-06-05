from django.contrib import admin
from django.urls import path, include
from tracker.views import index  # <-- import your index view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tracker.urls')),  # your API endpoints
    path('', index, name='home'),          # root URL shows your HTML page
]

