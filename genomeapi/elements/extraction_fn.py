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
   This is basic operations for extraction function

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

from .element import Element
from .exceptions import APIException

class SubStringFn(Element):
  def __call__(self, index: int, length: int):
    self.v = self.form_obj(index=index, length=length, type='substring')
    return self.v

class TimeFormatFn(Element):
  def __call__(self, format: str, timezone: str = 'UTC', locale: str = 'en'):
    self.v = self.form_obj(format=format, timeZone=timezone, locale=locale, type='timeFormat')
    return self.v

class ExtractionFn:
  fns = {'substring': SubStringFn, 'timeFormat': TimeFormatFn}
  def __new__(cls, typ='substring'):
    cls.typ = typ
    if typ in cls.fns.keys():
      return cls.fns[typ]()
    else:
      raise APIException("input type not recognized")

