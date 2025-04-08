from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ws/', include('api.urls')),  # Assure-toi que cette ligne est présente
]