__author__ = 'jingxuan'
from .basic_query import BasicQuery


class ODMatrix(BasicQuery):
  def __init__(self, token):
    super().__init__(end_point='odmatrix', token=token)
