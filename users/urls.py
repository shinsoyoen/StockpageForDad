from django.contrib import admin
from django.urls import path, include
from django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('transaction_History.urls')),
]
