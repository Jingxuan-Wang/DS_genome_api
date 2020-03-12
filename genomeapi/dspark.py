__author__ = 'jingxuan'
"""
This is a python package that is used to query Dspark mobility genome API
"""
from genomeapi.config import Config
from genomeapi.api import Authorize, DiscreteVisit, LinkMeta, ODMatrix, ODThroughLink, StayPoint

class Dspark:
  _URL = "https://apistore.dsparkanalytics.com.au"

  def __init__(self,
               token=None,
               site: str = "DEFAULT",
               ):
    if token is None:
      ## token not given, trying to fetch with given consumer_key and secret
      self.config = Config(site)

      self.auth = Authorize(url=self._URL+"/token",
                            consumer_key=self.config.consumer_key,
                            consumer_secret=self.config.consumer_secret)
      _token = self.auth._token
    else:
      ## token is given, use the token directly
      _token = token

    self.stay_point = StayPoint(_token)
    self.link_meta = LinkMeta(_token)
    self.discrete_visit = DiscreteVisit(_token)
    self.od_matrix = ODMatrix(_token)
    self.od_through_link = ODThroughLink(_token)
