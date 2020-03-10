__author__ = 'jingxuan'
"""
This is a python package that is used to query Dspark mobility genome API
"""
from genomeapi.config import Config
from genomeapi.api import Authorize, DiscreteVisit, LinkMeta, ODMatrix, ODThroughLink, StayPoint

class Dspark:
  _URL = "https://apistore.dsparkanalytics.com.au"

  def __init__(self,
               site: str = "DEFAULT",
               ):
    self.config = Config(site)

    self.auth = Authorize(self._URL+"/token", self.config.consumer_key, self.config.consumer_secret)

    self.stay_point = StayPoint(self.auth._token)
    self.link_meta = LinkMeta(self.auth._token)
    self.discrete_visit = DiscreteVisit(self.auth._token)
    self.od_matrix = ODMatrix(self.auth._token)
    self.od_through_link = ODThroughLink(self.auth._token)
