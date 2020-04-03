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
   This is basic operations for granularity

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

import re

from .element import Element
from .exceptions import APIException

class Granularity(Element):
  _TYPES = ['period']
  _FORMAT = r'^P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d+[HMS])(\d+H)?(\d+M)?(\d+S)?)?$'

  def validating(self, period, typ):
    if typ not in self._TYPES:
      raise APIException("wrong type for granularity")
    elif not re.fullmatch(self._FORMAT, period):
      raise APIException("wrong format for the period")
    elif "M" in period:
      mins = re.findall(r"(\d+)M", period)[0]
      if int(mins)%15 != 0:
        raise APIException("Period must be defined in buckets of 15 minutes")

  def __call__(self, period, typ):
    self.validating(period, typ)
    value = self.form_obj(period=period, type=typ)
    return self.form_obj(queryGranularity=value)
