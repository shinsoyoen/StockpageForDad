from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/<int:trade_id>/", views.delete_trade, name="delete_trade"),
]