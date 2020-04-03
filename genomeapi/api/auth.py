#  Copyright © DataSpark Pte Ltd 2014 - 2020.
#
#  This software and any related documentation contain confidential and proprietary information of
#  DataSpark and its licensors (if any). Use of this software and any related documentation is
#  governed by the terms of your written agreement with DataSpark. You may not use, download or
#  install this software or any related documentation without obtaining an appropriate licence
#  agreement from DataSpark.
#
#  All rights reserved.

"""
   This is for authorization related operation

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

import base64

from requests import post
from requests.status_codes import codes

from genomeapi.elements import ResponseException

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