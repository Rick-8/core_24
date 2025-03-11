# bookings/models.py

from django.db import models


class Booking(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"Booking for {self.name} on {self.date}"

        return f"Booking for {self.name} on {self.date}"
