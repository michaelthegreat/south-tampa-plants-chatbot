from django.urls import path
from . import views

app_name = "chatbot"
urlpatterns = [
    path(
        '',
        views.south_tampa_plants,
        name='south_tampa_plants'
    ),
]
