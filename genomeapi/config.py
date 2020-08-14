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
   This is basic operations for configuration before starting query

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""
import sys
import os

import configparser
from threading import Lock

class Config:
  SETTING = None
  LOCK = Lock()

  def __init__(self, site: str):
    with Config.LOCK:
      if Config.SETTING is None:
        self.loading()

    self.config_value = dict(Config.SETTING.items(site))

    self.consumer_key = self.consumer_secret = None
    self.fetch_value()

  def fetch_value(self):
    try:
      ## env variables are missing
      if os.environ.get("consumer_key") is None and os.environ.get("consumer_secret") is None:
        [setattr(self, i, self.config_value[i]) for i in ["consumer_key", "consumer_secret"]]
      ## env variables are set
      else:
        [setattr(self, i, os.environ[i]) for i in ["consumer_key", "consumer_secret"]]
    except:
      raise Exception("please set consumer key and secret by ini file or setting env value")

  @classmethod
  def loading(cls):
    config = configparser.ConfigParser()
    module_dir = os.path.dirname(sys.modules[__name__].__file__)
    locations = [os.path.join(module_dir, "config/genome_api.ini"), "~/genome_api.ini"]
    existence = [i for i in locations if os.path.exists(i)]
    config.read(locations)
    print(config)
    cls.SETTING = config