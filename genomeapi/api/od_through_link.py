__author__ = 'jingxuan'

from .basic_query import BasicQuery


class ODThroughLink(BasicQuery):
  def __init__(self, token):
    super().__init__(end_point='odthroughlink', token=token)

