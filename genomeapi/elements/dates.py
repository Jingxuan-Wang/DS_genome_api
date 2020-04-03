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
   This is basic operations for date query

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

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
