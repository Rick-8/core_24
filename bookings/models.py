from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'date')  # Prevent multiple bookings per user per day

    def clean(self):
        # Check the number of bookings for the selected date
        bookings_count = Booking.objects.filter(date=self.date).count()
        if bookings_count >= 100:
            raise ValidationError("The maximum number of bookings for this date has been reached.")

    def save(self, *args, **kwargs):
        # Call the clean method to check for the booking limit before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
