from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import *


@receiver(pre_delete, sender=UserVotes)
def dec_choice_vote(sender, instance, **kwargs):
    choice = instance.choice
    choice.votes -= 1
    choice.save()