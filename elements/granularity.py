__author__ = 'jingxuan'
from .element import Element
from .exceptions import APIException
import re

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
