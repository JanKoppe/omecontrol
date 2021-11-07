from django.conf import settings
from django.db import models

from omecontrol import ome_api_client

ome = ome_api_client.OmeApiClient(settings.OME_API_BASE, settings.OME_API_ACCESSTOKEN)

class PushConfig(models.Model):
  PROTOCOLS = (
    ('rtmp', 'RTMP'),
  )

  name = models.CharField(max_length=50)
  vhost = models.CharField(max_length=50, default='default')
  app = models.CharField(max_length=50, default='app')
  stream = models.CharField(max_length=50)
  url = models.CharField(max_length=256)
  streamkey = models.CharField(max_length=512)
  protocol = models.CharField(max_length=4, choices=PROTOCOLS, default='rtmp')
  active = models.BooleanField(default=True)
  notes = models.TextField(default='')

  def update_in_ome(self):
    # Let's take a look what OME does know already about this pushconfig
    push = ome.get_push(self.id, self.vhost, self.app)

    if self.active:
      # If it's active, it needs to be in OME
      if push is not None and \
        (
          push.get('stream').get('name') != self.stream or \
          push.get('protocol') != self.protocol or \
          push.get('url') != self.url or \
          push.get('streamKey') != self.streamkey \
        ):
          # push existed previously, but some setting changed - remove wrong config first
          ome.stop_push(str(self.id), self.vhost, self.app)
      # add pushconfig to OME
      ome.start_push(str(self.id), self.vhost, self.app, self.stream, self.url, self.streamkey, self.protocol)

    else:
      if push is not None:
        # If it should not be active, but OME has it configured, stop/remove the push!
        ome.stop_push(str(self.id), self.vhost, self.app)
  
  def delete_in_ome(self):
    # Let's take a look what OME does know already about this pushconfig
    push = ome.get_push(self.id, self.vhost, self.app)
    if push is not None:
      ome.stop_push(str(self.id), self.vhost, self.app)
  

