from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField()  # Users can pick a date

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    membership_number = models.CharField(max_length=50, unique=True, blank=True)
    personal_address = models.TextField()
    phone_number_1 = models.CharField(max_length=15)
    phone_number_2 = models.CharField(max_length=15)

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
            self.membership_number = self.generate_membership_number()  # Auto-generate if not set
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name()
