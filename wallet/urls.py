from django.urls import path
from .views import *

urlpatterns = [
    path('add_funds/', add_funds, name='add_funds'),  
    path('<int:user_id>/balance/', get_wallet_balance, name='get_wallet_balance'),  
]