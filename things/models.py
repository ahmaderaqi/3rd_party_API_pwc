from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=255)
    rank = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Flight(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    airline = models.CharField(max_length=255)
    flight_number = models.CharField(max_length=255)
    departure_airport_code = models.CharField(max_length=10)
    departure_airport_name = models.CharField(max_length=255)
    departure_latitude = models.FloatField()
    departure_longitude = models.FloatField()
    arrival_airport_code = models.CharField(max_length=10)
    arrival_airport_name = models.CharField(max_length=255)
    arrival_latitude = models.FloatField()
    arrival_longitude = models.FloatField()

    def __str__(self):
        return self.flight_number


class Weather(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()

    def __str__(self):
        return f"Weather for {self.event.title}"
