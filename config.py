__author__ = 'jingxuan'
"""
Setting Configuration for Dspark API
"""
import configparser
import sys
import os

from threading import Lock

class _NotSet(object):
  def __bool__(self):
    return False

  def __str__(self):
    return "NotSet"

class Config:

  CONFIG = None
  CONFIG_NOT_SET = _NotSet()
  LOCK = Lock()

  @classmethod
  def _load_config(cls):
    config = configparser.ConfigParser()
    module_dir = os.path.dirname(sys.modules[__name__].__file__)
    if "APPDATA" in os.environ: # Windows
      os_config_path = os.environ["APPDATA"]
    elif "XDG_CONFIG_HOME" in os.environ: # Modern Linux
      os_config_path = os.environ["XDG_CONFIG_HOME"]
    elif "HOME" in os.environ: # Legacy Linux
      os_config_path = os.path.join(os.environ["HOME"], ".config")
    else:
      os_config_path = None
    locations = [os.path.join(module_dir, "config/genome_api.ini"), "genome_api.ini"]
    if os_config_path is not None:
      locations.insert(1, os.path.join(os_config_path, "genome_api.ini"))
    config.read(locations)
    cls.CONFIG = config

  def __init__(self, site_name: str, **settings):
    # make sure all the instances share the same attribute value
    with Config.LOCK:
      if Config.CONFIG is None:
        self._load_config()

    self._settings = settings
    self.custom = dict(Config.CONFIG.items(site_name), **settings)

    self.consumer_key = self.consumer_secret = None
    self._initialize_attributes()

  def _initialize_attributes(self):
    for attribute in (
        "consumer_key",
        "consumer_secret",
    ):
      setattr(self, attribute, self._fetch_or_not_set(attribute))

  def _fetch(self, key: str):
    value = self.custom[key]
    return value

  def _fetch_default(self, key: str, default=None):
    if key not in self.custom:
      return default
    return self._fetch(key)

  def _fetch_or_not_set(self, key: str):
    if key in self._settings:
      return self._fetch(key)
    
    env_value = os.getenv("genome-api_{}".format(key))
    ini_value = self._fetch_default(key)

    return env_value or ini_value or self.CONFIG_NOT_SET

