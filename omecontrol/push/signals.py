from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from . import models

@receiver(post_save, sender=models.PushConfig)
def push_config_post_save_handler(sender, **kwargs):
  kwargs.get('instance').update_in_ome()

@receiver(pre_delete, sender=models.PushConfig)
def push_config_pre_delete_handler(sender, **kwargs):
  kwargs.get('instance').delete_in_ome()
