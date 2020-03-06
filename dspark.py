__author__ = 'jingxuan'
"""
This is a python package that is used to query Dspark mobility genome API
"""
import os
import configparser
from genome_api.config import Config
from genome_api.api import Authorize, DiscreteVisit, LinkMeta, ODMatrix, ODThroughLink, StayPoint
from genome_api.elements import ClientException

class Dspark:
  _URL = "https://apistore.dsparkanalytics.com.au"

  def __init__(self,
               site_name: str = "DEFAULT",
               **config_settings
               ):
    try:
      config_section = site_name or os.getenv("api_config")
      self.config = Config(config_section, **config_settings)
    except configparser.NoSectionError as exc:
      help_message = (
        "You provided the name of a genome-api.ini configuration which does not exist."
      )
      if site_name is not None:
        exc.message += "\n" + help_message
      raise

    required_message = """
      Reqired configuration setting {!r} missing. \n
      This setting can be provided in a genome-api.ini file,
      as a keyword argument to the `Dspark` class constructor,
      or as an enviorment variable.
    """

    for attribute in ("consumer_key", "consumer_secret"):
      if getattr(self.config, attribute) in (
        self.config.CONFIG_NOT_SET,
        None
      ):
        raise ClientException(required_message.format(attribute))

    self.auth = Authorize(self._URL+"/token", self.config.consumer_key, self.config.consumer_secret)
    self.auth.request_token()
    
    self.stay_point = StayPoint(self.auth.access_token)
    self.link_meta = LinkMeta(self.auth.access_token)
    self.discrete_visit = DiscreteVisit(self.auth.access_token)
    self.od_matrix = ODMatrix(self.auth.access_token)
    self.od_through_link = ODThroughLink(self.auth.access_token)
