from django.urls import path
from .views import *

urlpatterns = [
    path('purchase/', purchase_ticket, name='purchase_ticket'),
]
