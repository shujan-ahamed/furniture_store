from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User, UserProfile


@receiver(post_save, sender = User)
def post_save_create_profile_reciever(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
        print("userprofile created.")
    else:
        try:
            profile = UserProfile.objects.get(user = instance)
            profile.save()
            print("userprofile updated.")
        except:
            UserProfile.objects.create(user = instance)
            print("userprofile created on new.")


    