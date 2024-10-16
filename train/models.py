from django.db import models
from station.models import Station
from django.core.exceptions import ValidationError

# Create your models here.

class Train(models.Model):
    name = models.CharField(max_length=100)
    schedule = models.DateTimeField()



class TrainStop(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='stops')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    stop_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Ensuring stop time is after the train's schedule
        if self.stop_time <= self.train.schedule:
            raise ValidationError("Stop time must be after the train's departure time.")

        # Ensuring stop times are in order
        previous_stops = TrainStop.objects.filter(train=self.train).order_by('-stop_time')
        if previous_stops.exists():
            last_stop_time = previous_stops.first().stop_time
            if self.stop_time <= last_stop_time:
                raise ValidationError("Stop time must be later than the previous stop.")

        super(TrainStop, self).save(*args, **kwargs)

    class Meta:
        ordering = ['stop_time']


