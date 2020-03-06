__author__ = 'jingxuan'
from .element import Element
from .exceptions import APIException

class Dates(Element):
  def validating(self, value):
    if not isinstance(value, dict):
      raise APIException("the input argument is in wrong format")

  def __call__(self, begin_date, end_date=None):
    if not end_date:
      date = SingleDate()
      value = date(begin_date)
      self.validating(value)
      return self.form_obj(dates=value)
    else:
      dates = DateRange()
      value = dates(begin_date=begin_date, end_date=end_date)
      self.validating(value)
      return self.form_obj(dates=value)

class SingleDate(Element):
  def validating(self, date):
    if not isinstance(date, str):
      raise APIException("the input argument is in wrong format")

  def __call__(self, date):
    self.validating(date)
    return self.form_obj(value=date, type="single")

class DateRange(Element):
  def validating(self, begin_date, end_date):
    if not isinstance(begin_date, str) or not isinstance(end_date, str):
      raise APIException("the input argument is in wrong format")

  def __call__(self, begin_date, end_date):
    self.validating(begin_date, end_date)
    return self.form_obj(beginDate=begin_date, endDate=end_date, type="range")
