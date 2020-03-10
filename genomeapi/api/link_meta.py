__author__ = 'jingxuan'
from .basic_query import BasicQuery


class LinkMeta(BasicQuery):
  def __init__(self, token):
    super().__init__(end_point='linkmeta', token=token)

