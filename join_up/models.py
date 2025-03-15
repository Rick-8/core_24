from django.db import models
from ckeditor.fields import RichTextField


class Customer(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone_number_1 = models.CharField(max_length=15, blank=False)
    phone_number_2 = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = RichTextField()

    def __str__(self):
        return self.name
