__author__ = 'jingxuan'
from .element import Element

class Link(Element):
  def __call__(self, *links):
    value = list(links)
    return self.form_obj(links=value)