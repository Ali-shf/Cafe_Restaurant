from authentication.models import AdminProfile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=AdminProfile)
def make_user_staff(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.is_staff = True
        user.save(update_fields=['is_staff'])

