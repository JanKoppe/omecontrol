import base64
import requests
import json

class OmeApiClient():
  def __init__(self, base: str, accesstoken: str):
    self.base = base 
    self.s = requests.Session()

    headers = {'Authorization' : f"Basic {base64.b64encode(accesstoken.encode()).decode('utf-8')}"}
    self.s.headers.update(headers)

  def start_push(self, id: str, vhost: str, app: str, stream: str, url: str, streamkey: str, protocol: str = "rtmp" ) -> None:
    data = {
      'id': id,
      'stream': { 'name': stream },
      'protocol': protocol,
      'url': url,
      'streamKey': streamkey,
    }

    self.s.post(f"{self.base}/v1/vhosts/{vhost}/apps/{app}:startPush", json=data)

  def stop_push(self, id: str, vhost: str, app: str) -> None:
    data = {
      'id': id,
    }
    
    self.s.post(f"{self.base}/v1/vhosts/{vhost}/apps/{app}:stopPush", json=data)

  def get_push(self, id: str, vhost: str, app: str) -> any:
    pushes = self.list_pushes(vhost, app)

    for push in pushes:
      if str(push.get('id')) == str(id):
        return push

    return None

  def list_pushes(self, vhost: str, app: str) -> list:

    r = self.s.post(f"{self.base}/v1/vhosts/{vhost}/apps/{app}:pushes")
    
    if r.status_code == 204:
      return []

    pushes = r.json()['response']

    return pushes

