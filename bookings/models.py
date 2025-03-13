from django.db import models
from django.contrib.auth.models import User


class Booking(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)  # Link to the User model
    email = models.EmailField()  # Email field
    membership_number = models.CharField(max_length=20, null=True, blank=True)  # Membership number
    active_membership = models.BooleanField(default=True)  # Active membership status
    date = models.DateField()
    slot = models.CharField(max_length=100)
    # Add a name field to make the form work if needed
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date} - {self.slot}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    membership_number = models.CharField(max_length=50, unique=True)
    personal_address = models.TextField()
    phone_number_1 = models.CharField(max_length=15)
    phone_number_2 = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name()
