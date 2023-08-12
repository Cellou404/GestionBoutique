# code

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def CreateProfile(sender, instance, created, **kwargs):
    """ 
        ## Create Profile Signal

        When a new user is created, a new profile account is 
        also created.
    """
    print('Profile signal trigged')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    """ 
        ## Delete Profile Signal

        When a profile account is deleted, the user account will 
        also be deleted.
    """
    user = instance.user
    user.delete()

#post_save.connect(CreateProfile, sender=User)
#post_delete.connect(deleteUser, sender=Profile)