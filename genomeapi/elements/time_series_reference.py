__author__ = 'jingxuan'
from .element import Element

class TimeSeriesReference(Element):
  def __call__(self, v):
    return self.form_obj(timeSeriesReference=v)