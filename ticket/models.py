from django.db import models
from django.contrib.auth.models import User
from train.models import Train, TrainStop

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    stops = models.ManyToManyField(TrainStop)
    purchased_at = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)

