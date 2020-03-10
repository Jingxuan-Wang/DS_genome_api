__author__ = 'jingxuan'
"""
Basic Object for all query elements
"""

class Element:
  def __init__(self):
    pass

  def form_obj(self, **kwargs):
    return kwargs

  def __call__(self, *args, **kwargs):
    pass

  def validating(self, *args, **kwargs):
    pass
