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
   This is basic operations for aggregation

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

from .element import Element
from .exceptions import APIException

##TODO aggregation lack of extraction function

class Aggregation(Element):
  _NORMAL_TYPES = ['longSum', 'doubleSum', 'longMin', 'doubleMin', 'longMax', 'doubleMax', 'hyperUnique']

  def validating(self, typ):
    if typ not in self._NORMAL_TYPES:
      raise APIException("Sorry, we don't have such type for aggregation!")
    else:
      pass

  def __call__(self, metric, typ, described_as=None):
    self.validating(typ)
    value = self.form_obj(metric=metric, type=typ) if described_as is None else self.form_obj(
      metric=metric, type=typ, describedAs=described_as)
    self.aggs = [value]
    return self
  
  def __add__(self, other):
    self.aggs += other.aggs
    return self
  
  def to_dict(self):
    return self.form_obj(aggregations=self.aggs)

