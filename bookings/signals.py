from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Max


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a Profile whenever a User is saved.
    """
    if created:

        profile = Profile.objects.create(user=instance)

        last_membership_number = Profile.objects.aggregate(
            Max('membership_number')
        )['membership_number__max']

        if last_membership_number is None:
            new_membership_number = 1001
        else:
            new_membership_number = int(last_membership_number) + 1

        profile.membership_number = str(new_membership_number)
        profile.save()
    else:

        instance.profile.save()
