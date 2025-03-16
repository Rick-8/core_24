from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.core.exceptions import ValidationError


class Booking(models.Model):
    # ForeignKey to link the booking to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    # Date for the booking
    date = models.DateField()

    # Optional: Add a field to indicate if the gym is closed for maintenance on a specific day
    closed_for_maintenance = models.BooleanField(default=False)

    def clean(self):
        """
        Custom validation to ensure that no more than 50 bookings can be made for a given date.
        """
        if self.closed_for_maintenance:
            raise ValidationError(f"The gym is closed on {self.date}. No bookings can be made.")

        # Check if there are already 50 bookings for the selected date
        if Booking.objects.filter(date=self.date).count() >= 50:
            raise ValidationError("Booking limit reached for this date. Please select another date.")

    def save(self, *args, **kwargs):
        # Before saving, call the clean method to ensure validation
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {'Closed' if self.closed_for_maintenance else 'Open'}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    membership_number = models.CharField(max_length=50, unique=True, blank=True)
    personal_address = models.TextField()
    phone_number_1 = models.CharField(max_length=15)
    phone_number_2 = models.CharField(max_length=15,)

    def generate_membership_number(self):
        """
        Generates a unique membership number.
        Starts from 1001 and increments based on the highest existing membership number.
        """
        MEMBERSHIP_START_NUMBER = 1001
        latest_profile = Profile.objects.aggregate(Max('membership_number'))['membership_number__max']

        if latest_profile is None:
            new_membership_number = MEMBERSHIP_START_NUMBER
        else:
            new_membership_number = int(latest_profile) + 1

        return str(new_membership_number)

    def save(self, *args, **kwargs):
        if not self.membership_number:
            self.membership_number = self.generate_membership_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name()


class ClosedDay(models.Model):
    date = models.DateField(unique=True)
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.reason}"
