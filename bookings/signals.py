from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Max


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:  # Only create a profile if the user is newly created
        profile = Profile.objects.create(user=instance)

        # Generate the membership number for the new profile
        last_membership_number = Profile.objects.aggregate(Max('membership_number'))['membership_number__max']

        if last_membership_number is None:
            new_membership_number = 1001  # Starting membership number
        else:
            new_membership_number = int(last_membership_number) + 1  # Incrementing the last membership number

        # Assign the new membership number to the profile
        profile.membership_number = str(new_membership_number)  # Ensure it's a string
        profile.save()
    else:
        # Update the profile if the user is updated
        instance.profile.save()
