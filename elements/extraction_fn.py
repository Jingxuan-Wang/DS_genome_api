__author__ = 'jingxuan'

from .element import Element

class SubStringFn(Element):
  def __call__(self, index: int, length: int):
    self.v = self.form_obj(index=index, length=length, type='substring')
    return self.v

class TimeFormatFn(Element):
  def __call__(self, format: str, timezone: str = 'UTC', locale: str = 'en'):
    self.v = self.form_obj(format=format, timeZone=timezone, locale=locale, type='timeFormat')
    return self.v

class ExtractionFn:
  fns = {'string': SubStringFn, 'time': TimeFormatFn}
  def __new__(cls, typ='string'):
    cls.typ = typ
    if typ in cls.fns.keys():
      return cls.fns[typ]()
    else:
      raise APIException("input type not recognized")

