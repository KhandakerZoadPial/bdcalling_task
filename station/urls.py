from django.urls import path
from .views import *

urlpatterns = [
    path('create_station/', create_station, name='create_station'),
    path('get_stations/', get_stations, name='get_stations'),
    path('station_details/<int:station_id>', station_details, name='station_details')
]
