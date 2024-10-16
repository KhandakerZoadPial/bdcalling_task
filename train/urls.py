from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('train/', train, name='train'),
    path('train/<int:train_id>/', train, name='train_with_id'),
    path('create_train_stop/<int:train_id>/', create_train_stop, name='create_train_stop'),
    path('get_train_with_stops/<int:train_id>/', get_train_with_stops, name='get_train_with_stops')
]
