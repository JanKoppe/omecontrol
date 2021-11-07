from django.db import models

# Create your models here.


class Grant(models.Model):
  """
  A grant defines an explicit set of constraints that will return an Accept response
  on the Admission Webhook
  """
  DIRECTIONS = (
    ('incoming', 'incoming'),
    ('outgoing', 'outgoing'),
  )

  PROTOCOLS = (
    ('webrtc', 'WebRTC'),
    ('rtmp', 'RTMP'),
    ('srt', 'SRT'),
    ('hls', 'HLS'),
    ('dash', 'DASH'),
    ('lldash', 'LLDASH'),
  )

  direction = models.CharField(max_length=8, choices=DIRECTIONS, default='push')
  protocol = models.CharField(max_length=6, choices=PROTOCOLS, default='rtmp')
  application = models.CharField(max_length=50, default='default')
  name = models.CharField(max_length=50)
  secret = models.CharField(max_length=50)
  notes = models.TextField(default='')

  def __str__(self):
    return f"{self.direction} - {self.protocol}:{self.application}:{self.name}"