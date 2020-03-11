__author__ = 'jingxuan'
from genomeapi.elements import ResponseException, RequestException

import time
from requests import post
from requests.status_codes import codes
import base64

class Authorize:
  
  def __init__(self, url: str, consumer_key: str = "", consumer_secret: str = ""):
    self._token = None
    self._scopes = None
    self._url = url
    self.get_token(consumer_key, consumer_secret)

  def get_token(self, consumer_key:str, consumer_secret:str):
    keySecret = (consumer_key + ":" + consumer_secret).encode('utf-8')
    consumerKeySecretB64 = base64.b64encode(keySecret).decode('utf-8')
    response = post("https://apistore.dsparkanalytics.com.au/token",
                                  data={'grant_type': 'client_credentials'},
                                  headers={'Authorization': 'Basic ' + consumerKeySecretB64})
    if response.status_code != codes["ok"]:
      raise ResponseException(response)
    result = response.json()
    self._token = result['access_token']
    self._scopes = set(result['scope'].split(" "))

  def clear(self):
    self._token = None