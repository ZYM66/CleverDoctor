from django.urls import path
from .views import room

urlpatterns = [
    # path('', views.index, name='index'),
    path('<str:room_name>/', room.as_view(), name='room'),
]

