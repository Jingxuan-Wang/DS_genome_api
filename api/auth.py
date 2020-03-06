__author__ = 'jingxuan'
from genome_api.elements import ResponseException

import time
from requests import post
from requests.auth import HTTPBasicAuth
from requests.status_codes import codes

class Authorize:
  
  def __init__(self, url: str, consumer_key: str, consumer_secret: str):
    self.access_token = None
    self.scopes = None
    self._expiration_timestamp = None
    self._url = url
    self._consumer_key = consumer_key
    self._consumer_secret = consumer_secret
  
  def request_token(self):
    pre_request_timestamp = time.time() 
    response = post(self._url, auth=HTTPBasicAuth(self._consumer_key, self._consumer_secret), 
                    data={'grant_type': 'client_credentials'})
    if response.status_code != codes["ok"]:
      raise ResponseException(response)
    payload = response.json()
    self._expiration_timestamp = (
      pre_request_timestamp - 10 + payload['expires_in']
    )

    self.access_token = payload['access_token']
    self.scopes = set(payload['scope'].split(" "))

  def _clear_token(self):
    self.access_token = None