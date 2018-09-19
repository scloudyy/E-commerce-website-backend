from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

# don't work in the previous
# https://stackoverflow.com/questions/43322188/runtimeerror-model-class-django-messages-models-message-doesnt-declare-an-expl


@receiver(post_save, sender=User)
def encode_password(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
