from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST 

from . import models

import json
from urllib.parse import urlparse, parse_qs

@csrf_exempt
@require_POST
def admission(request: HttpRequest) -> JsonResponse:

  try:
    d = json.loads(request.body.decode('utf-8'))
    r = d.get('request')
  except json.JSONDecodeError:
    return JsonResponse({'allowed': False})

  url = urlparse(r['url'])

  parts = url.path.split('/')
  application = parts[1]
  stream = parts[2]
  queries = parse_qs(url.query)
  secret = queries['secret'][0]

  try:
    models.Grant.objects.get(
      direction=r['direction'].lower(),
      protocol=r['protocol'].lower(),
      application=application,
      name=stream,
      secret=secret 
      )
  except models.Grant.DoesNotExist:
    return JsonResponse({'allowed': False})

  return JsonResponse({'allowed': True})