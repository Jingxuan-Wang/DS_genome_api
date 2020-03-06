__author__ = 'jingxuan'
from .element import Element
from .exceptions import APIException

class Aggregation(Element):
  _NORMAL_TYPES = ['longSum', 'doubleSum', 'longMin', 'doubleMin', 'longMax', 'doubleMax', 'hyperUnique']

  def validating(self, metric, typ):
    if typ not in self._NORMAL_TYPES:
      raise APIException("Sorry, we don't have such type for aggregation!")
    else:
      pass

  def __call__(self, metric, typ, described_as=None):
    self.validating(metric, typ)
    value = self.form_obj(metric=metric, type=typ) if described_as == None else self.form_obj(
      metric=metric, type=typ, describedAs=described_as)
    self.aggs = [value]
    return self
  
  def __add__(self, other):
    self.aggs += other.aggs
    return self
  
  def to_dict(self):
    return self.form_obj(aggregations=self.aggs)

