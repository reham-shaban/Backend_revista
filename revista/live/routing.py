from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/live/<int:live_id>/', consumers.LiveVideoConsumer.as_asgi()),
]