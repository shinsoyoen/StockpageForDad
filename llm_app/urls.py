from django.urls import path
from .views import chatbot_page

urlpatterns = [
    path("page/", chatbot_page, name="chatbot_page"),
]